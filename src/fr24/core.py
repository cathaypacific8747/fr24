from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, BinaryIO, Literal

import httpx
import pyarrow as pa
import pyarrow.compute as pc
from appdirs import user_cache_dir
from loguru import logger
from typing_extensions import Self, override

import pandas as pd

from .base import APIResponse, ArrowTable, HTTPClient, ServiceBase
from .common import to_unix_timestamp
from .grpc import (
    live_feed_playback_world_data,
    live_feed_world_data,
)
from .json import (
    flight_list,
    flight_list_arrow,
    playback,
    playback_arrow,
)
from .types.authentication import TokenSubscriptionKey, UsernamePassword
from .types.cache import (
    LiveFeedRecord,
    flight_list_schema,
    live_feed_schema,
    playback_track_schema,
)
from .types.core import (
    FlightListContext,
    LiveFeedContext,
    PlaybackContext,
)
from .types.flight_list import FlightList
from .types.fr24 import LiveFeedField
from .types.playback import FlightData, Playback


class FR24:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *,
        base_dir: str = user_cache_dir("fr24"),
    ) -> None:
        """
        See docs [quickstart](../usage/quickstart.md#initialisation).

        :param client: The `httpx` client to use. If not provided, a
            new one will be created with HTTP/2 enabled by default. It is
            highly recommended to use `http2=True` to avoid
            [464 errors](https://github.com/cathaypacific8747/fr24/issues/23#issuecomment-2125624974)
            and to be consistent with the browser.
        :param base_dir:
            See [cache directory](../usage/cli.md#directories).
        """
        self.http = HTTPClient(
            httpx.AsyncClient(http2=True) if client is None else client
        )
        self._base_dir = Path(base_dir)
        self.flight_list = FlightListService(self.http, self._base_dir)
        self.playback = PlaybackService(self.http, self._base_dir)
        self.live_feed = LiveFeedService(self.http, self._base_dir)

    async def login(
        self,
        creds: (
            TokenSubscriptionKey | UsernamePassword | None | Literal["from_env"]
        ) = "from_env",
    ) -> None:
        """
        :param creds: Reads credentials from the environment variables or the
            config file if `creds` is set to `"from_env"` (default). Otherwise,
            provide the credentials directly.
        """
        await self.http._login(creds)

    @property
    def base_dir(self) -> Path:
        return self._base_dir

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


class FlightListAPI:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http

    async def _fetch(
        self,
        ctx: FlightListContext,
        page: int,
        limit: int,
        timestamp: int | datetime | pd.Timestamp | str | None,
    ) -> FlightList:
        if ctx["kind"] == "reg":
            reg, flight = ctx["ident"], None
        else:
            reg, flight = None, ctx["ident"]
        return await flight_list(
            self.http.client,
            reg,
            flight,
            page,
            limit,
            timestamp,
            self.http.auth,
        )

    async def _fetch_all(
        self,
        ctx: FlightListContext,
        page: int,
        limit: int,
        timestamp: int | datetime | pd.Timestamp | str | None,
        delay: int,
    ) -> AsyncIterator[FlightList]:
        more = True
        while more:
            fl = await self._fetch(ctx, page, limit, timestamp)

            # shouldn't happen, but stop in case we overshot
            if (data := fl["result"]["response"]["data"]) is None:
                break

            yield fl

            # NOTE: for the next request, we have to both:
            # - update the timestamp to the earliest STD in the current batch
            # - increment the page
            # weird, but it's how the API works
            timestamp = min(
                t
                for d in data
                if (t := d["time"]["scheduled"]["departure"]) is not None
            )
            page += 1
            more = fl["result"]["response"]["page"]["more"]
            await asyncio.sleep(delay)


class FlightListAPIResp(APIResponse[FlightListContext, FlightList]):
    """A wrapper around the flight list API response."""

    def to_arrow(self) -> FlightListArrow:
        """
        Parse each [fr24.types.flight_list.FlightListItem][] in the API response
        and transform it into a pyarrow.Table.
        """
        return FlightListArrow(
            self.ctx, flight_list_arrow(self.data)
        )  # NOTE: use constructor?


class FlightListArrow(ArrowTable[FlightListContext]):
    """A wrapper around a pyarrow.Table containing flight list data."""

    @classmethod
    def from_cache(cls, ctx: FlightListContext) -> FlightListArrow:
        fp = FlightListArrow._fp(ctx)
        return super(FlightListArrow, cls).from_file(
            ctx, fp, flight_list_schema
        )

    @classmethod
    def _fp(cls, ctx: FlightListContext) -> Path:
        return (
            ctx["base_dir"]
            / "flight_list"
            / ctx["kind"]
            / f"{ctx['ident'].upper()}.parquet"
        )

    @override
    def concat(
        self,
        data_new: FlightListArrow,  # | FlightListAPIResp,
        inplace: bool = False,
    ) -> FlightListArrow:
        """
        Returns a new list of flights merged with the current table.
        Duplicates are removed from the current table, which results in
        all `Estimated` flights to be updated with the new data (if any).

        :param inplace: If `True`, the current table will be updated in place.
        """
        # TODO: allow passing list[arrow|apiresp]
        # if isinstance(data_new, FlightListAPIResp):
        #     data_new = data_new.to_arrow()
        mask: pa.ChunkedArray = pc.is_in(
            self.data["flight_id"], value_set=data_new.data["flight_id"]
        )
        if (dup_count := pc.sum(mask).as_py()) is not None and dup_count > 0:
            logger.info(f"overwriting {dup_count} duplicate flight ids")
        data = pa.concat_tables(
            [self.data.filter(pc.invert(mask.combine_chunks())), data_new.data]
        )
        if inplace:
            self.data = data
            return self
        return FlightListArrow(self.ctx, data)

    @override
    def save(
        self,
        fp: Path | BinaryIO | None = None,
        fmt: Literal["parquet", "csv"] = "parquet",
    ) -> Self:
        """
        Write the table to the given file path or file-like object,
        e.g. `./tmp/foo.parquet`, `sys.stdout.buffer`.

        :param fp: File path to save the table to. If `None`, the table will
            be saved to the appropriate cache directory.

        :raises ValueError: If a format other than `parquet` is provided when
            saving to cache.
        """
        if fp is None and fmt != "parquet":
            raise ValueError("format must be `parquet` when saving to cache")
        super().save(
            fp if fp is not None else FlightListArrow._fp(self.ctx), fmt
        )
        return self


class FlightListService(ServiceBase):
    """A service to handle the flight list API and file operations."""

    def __init__(self, http: HTTPClient, base_dir: Path) -> None:
        self._http = http
        self._base_dir = base_dir
        self._api = FlightListAPI(http)

    async def fetch(
        self,
        *,
        reg: str | None = None,
        flight: str | None = None,
        page: int = 1,
        limit: int = 10,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
    ) -> FlightListAPIResp:
        """
        Fetch one page of flight list for the given registration or
        flight number.

        *Related: [fr24.json.flight_list][]*

        Input **either** the registration or the flight number, not both.

        :param reg: Aircraft registration (e.g. `B-HUJ`)
        :param flight: Flight number (e.g. `CX8747`)
        :param limit: Number of flights per page - use `100` if authenticated
        :param timestamp: Show flights with ATD before this Unix timestamp
        """
        ctx = self._construct_ctx(reg, flight)
        return FlightListAPIResp(
            ctx, await self._api._fetch(ctx, page, limit, timestamp)
        )

    async def fetch_all(
        self,
        *,
        reg: str | None = None,
        flight: str | None = None,
        page: int = 1,
        limit: int = 10,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
        delay: int = 5,
    ) -> AsyncIterator[FlightListAPIResp]:
        """
        Iteratively fetch all pages of the flight list for the given
        registration or flight number.

        *Related: [fr24.json.flight_list][]*

        Input **either** the registration or the flight number, not both.

        :param reg: Aircraft registration (e.g. `B-HUJ`)
        :param flight: Flight number (e.g. `CX8747`)
        :param limit: Number of flights per page - use `100` if authenticated
        :param timestamp: Show flights with ATD before this Unix timestamp
        :param delay: Delay between requests in seconds
        """
        ctx = self._construct_ctx(reg, flight)
        async for raw in self._api._fetch_all(
            ctx, page, limit, timestamp, delay
        ):
            yield FlightListAPIResp(ctx, raw)

    def load(
        self, *, reg: str | None = None, flight: str | None = None
    ) -> FlightListArrow:
        """
        Get flight list for the given registration or flight number from
        the [cache](../usage/cli.md#directories). If the file does not exist,
        an empty table will be returned.

        Input **either** the registration or the flight number, not both.
        """
        # TODO: allow passing list[str] and call .concat() underneath
        ctx = self._construct_ctx(reg, flight)
        return FlightListArrow.from_cache(ctx)

    def _construct_ctx(
        self, reg: str | None, flight: str | None
    ) -> FlightListContext:
        if reg is not None and flight is None:
            return {"ident": reg, "kind": "reg", "base_dir": self._base_dir}
        if reg is None and flight is not None:
            return {
                "ident": flight,
                "kind": "flight",
                "base_dir": self._base_dir,
            }
        raise ValueError(
            "expected one of `reg` or `flight` to be set, not both or neither."
        )


class PlaybackAPI:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http

    async def _fetch(
        self,
        ctx: PlaybackContext,
        timestamp: int | datetime | pd.Timestamp | str | None = None,
    ) -> Playback:
        """
        Fetch the historical track playback data for the given flight.

        *Related: [fr24.json.playback][]*

        :param timestamp: Unix timestamp (seconds) of ATD - optional, but
            it is recommended to include it
        """
        return await playback(
            self.http.client, ctx["flight_id"], timestamp, self.http.auth
        )


class PlaybackApiResp(APIResponse[PlaybackContext, Playback]):
    """A wrapper around the playback API response."""

    def to_arrow(self) -> PlaybackArrow:
        """
        Parse each [fr24.types.playback.TrackData][] in the API response and
        transform it into a wrapped pyarrow.Table. Also adds
        [fr24.types.playback.FlightData][] into the schema's metadata with key
        `_flight`.
        """
        return PlaybackArrow(self.ctx, playback_arrow(self.data))


class PlaybackArrow(ArrowTable[PlaybackContext]):
    """Arrow table for playback data."""

    @classmethod
    def from_cache(cls, ctx: PlaybackContext) -> PlaybackArrow:
        fp = PlaybackArrow._fp(ctx)
        return super(PlaybackArrow, cls).from_file(
            ctx, fp, playback_track_schema
        )

    @classmethod
    def _fp(cls, ctx: PlaybackContext) -> Path:
        return ctx["base_dir"] / "playback" / f"{ctx['flight_id']}.parquet"

    @override
    def concat(
        self, data_new: PlaybackArrow, inplace: bool = False
    ) -> PlaybackArrow:
        raise NotImplementedError(
            "playback of fr24 flight tracks cannot be concatenated together, "
            "use `xoolive/traffic` if you need to merge tracks."
        )

    @override
    def save(
        self,
        fp: Path | BinaryIO | None = None,
        fmt: Literal["parquet", "csv"] = "parquet",
    ) -> Self:
        """
        Write the table to the given file path or file-like object,
        e.g. `./tmp/foo.parquet`, `sys.stdout.buffer`.

        :param fp: File path to save the table to. If `None`, the table will
            be saved to the appropriate cache directory.

        :raises ValueError: If a format other than `parquet` is provided when
            saving to cache.
        """
        if fp is None and fmt != "parquet":
            raise ValueError("format must be `parquet` when saving to cache")
        super().save(fp if fp is not None else PlaybackArrow._fp(self.ctx), fmt)
        return self

    @property
    def metadata(self) -> FlightData | None:
        """Parse the flight metadata from the arrow table."""
        if m := self.data.schema.metadata.get(b"_flight"):
            return json.loads(m)  # type: ignore[no-any-return]
        return None


class PlaybackService(ServiceBase):
    """A service to handle the playback API and file operations."""

    def __init__(self, http: HTTPClient, base_dir: Path) -> None:
        self._http = http
        self._base_dir = base_dir
        self._api = PlaybackAPI(http)

    async def fetch(
        self,
        flight_id: str | int,
        timestamp: int | datetime | pd.Timestamp | str | None = None,
    ) -> PlaybackApiResp:
        """
        Fetch the historical track playback data for the given flight.

        *Related: [fr24.json.playback][]*

        :param flight_id: Hex Flight ID (e.g. `"2d81a27"`, `0x2d81a27`)
        :param timestamp: Unix timestamp (seconds) of ATD - optional, but
            it is recommended to include it
        """
        ctx = self._construct_ctx(flight_id)
        return PlaybackApiResp(
            ctx, await self._api._fetch(ctx, timestamp=timestamp)
        )

    def load(self, flight_id: str | int) -> PlaybackArrow:
        """
        Get playback data for the given flight ID from the
        [cache](../usage/cli.md#directories). If the file does not exist,
        an empty table will be returned.
        """
        ctx = self._construct_ctx(flight_id)
        return PlaybackArrow.from_cache(ctx)

    def _construct_ctx(self, flight_id: str | int) -> PlaybackContext:
        if not isinstance(flight_id, str):
            flight_id = f"{flight_id:x}"
        flight_id = flight_id.lower()
        return {"flight_id": flight_id, "base_dir": self._base_dir}


class LiveFeedAPI:
    def __init__(self, http: HTTPClient) -> None:
        self.http = http

    async def _fetch(
        self,
        ctx: LiveFeedContext,
    ) -> list[LiveFeedRecord]:
        kw = {
            k: v
            for k, v in ctx.items()
            if k in ("limit", "fields") and v is not None
        }
        if (ts := ctx["timestamp"]) is not None:
            kw.update(
                {
                    k: v
                    for k, v in ctx.items()
                    if k in ("duration", "hfreq") and v is not None
                }
            )
            return await live_feed_playback_world_data(
                self.http.client,
                ts,
                **kw,  # type: ignore[arg-type]
                auth=self.http.auth,
            )
        resp = await live_feed_world_data(
            self.http.client,
            self.http.auth,
            **kw,  # type: ignore[arg-type]
        )
        ctx["timestamp"] = int(time.time())
        # TODO: use server time instead, but it doesn't really matter because
        # live feed messages have timestamps attached to them anyway
        return resp


class LiveFeedAPIResp(APIResponse[LiveFeedContext, list[LiveFeedRecord]]):
    """A wrapper around the live feed API response."""

    def to_arrow(self) -> LiveFeedArrow:
        """
        Parse each [fr24.types.cache.LiveFeedRecord][] in the API response and
        transform it into a wrapped pyarrow.Table.
        """
        if len(self.data) == 0:
            logger.warning("no data in response, table will be empty")
        table = pa.Table.from_pylist(
            self.data,
            schema=live_feed_schema,
        )
        return LiveFeedArrow(self.ctx, table)


class LiveFeedArrow(ArrowTable[LiveFeedContext]):
    """Arrow table for live feed data."""

    @classmethod
    def from_cache(cls, ctx: LiveFeedContext) -> LiveFeedArrow:
        fp = LiveFeedArrow._fp(ctx)
        return super(LiveFeedArrow, cls).from_file(ctx, fp, live_feed_schema)

    @classmethod
    def _fp(cls, ctx: LiveFeedContext) -> Path:
        ts = ctx["timestamp"]
        assert ts is not None, (
            "tried to get a cached snapshot of the live feed, but the "
            "timestamp was not provided."
        )
        return ctx["base_dir"] / "feed" / f"{ts}.parquet"

    @override
    def concat(
        self, data_new: LiveFeedArrow, inplace: bool = False
    ) -> LiveFeedArrow:
        raise NotImplementedError(
            "live feed data cannot be concatenated together"
        )

    @override
    def save(
        self,
        fp: Path | BinaryIO | None = None,
        fmt: Literal["parquet", "csv"] = "parquet",
    ) -> Self:
        """
        Write the table to the given file path or file-like object,
        e.g. `./tmp/foo.parquet`, `sys.stdout`.

        :param fp: File path to save the table to. If `None`, the table will
            be saved to the appropriate cache directory.

        :raises ValueError: If a format other than `parquet` is provided when
            saving to cache.
        """
        if fp is None and fmt != "parquet":
            raise ValueError("format must be `parquet` when saving to cache")
        super().save(fp if fp is not None else LiveFeedArrow._fp(self.ctx), fmt)
        return self


class LiveFeedService(ServiceBase):
    """A service to handle the live feed API and file operations."""

    def __init__(self, http: HTTPClient, base_dir: Path) -> None:
        self._http = http
        self._base_dir = base_dir
        self._api = LiveFeedAPI(http)

    async def fetch(
        self,
        timestamp: int | str | datetime | pd.Timestamp | None = None,
        *,
        duration: int | None = None,
        hfreq: int | None = None,
        limit: int = 1500,
        fields: list[LiveFeedField] = [
            "flight",
            "reg",
            "route",
            "type",
        ],
    ) -> LiveFeedAPIResp:
        """
        Fetch live feed data.

        *Related: [fr24.grpc.live_feed_world_data][]*

        :param timestamp: Unix timestamp (seconds) of the live feed data.
            If `None`, the latest live data will be fetched. Otherwise,
            historical data will be fetched instead.
        :param duration: Prefetch duration (default: `7` seconds). Should only
            be set for historical data.
        :param hfreq: High frequency mode (default: `0`). Should only be set
            for historical data.
        :param limit: Max number of flights (default 1500 for unauthenticated
            users, 2000 for authenticated users)
        :param fields: fields to include - for unauthenticated users, max 4
            fields. When authenticated, `squawk`, `vspeed`, `airspace`,
            `logo_id` and `age` can be included
        """
        ctx = self._construct_ctx(timestamp, duration, hfreq, limit, fields)
        return LiveFeedAPIResp(ctx, await self._api._fetch(ctx))

    def load(
        self,
        timestamp: int | str | datetime | pd.Timestamp,
    ) -> LiveFeedArrow:
        """
        Get live feed data from the
        [cache](../usage/cli.md#directories). If the file does not exist,
        an empty table will be returned.

        :param timestamp: Unix timestamp (seconds) of the saved feed snapshot.
        """
        ctx = self._construct_ctx(timestamp, None, None, None, None)
        return LiveFeedArrow.from_cache(ctx)

    def _construct_ctx(
        self,
        timestamp: int | str | datetime | pd.Timestamp | None,
        duration: int | None,
        hfreq: int | None,
        limit: int | None,
        fields: list[LiveFeedField] | None,
    ) -> LiveFeedContext:
        ts = to_unix_timestamp(timestamp)
        if ts is None and (hfreq is not None or duration is not None):
            raise ValueError(
                "`hfreq` and `duration` can only be set for historical data."
            )
        return {
            "timestamp": ts,
            "source": "live" if ts is None else "playback",
            "duration": duration,
            "hfreq": hfreq,
            "limit": limit,
            "fields": fields,
            "base_dir": self._base_dir,
        }
