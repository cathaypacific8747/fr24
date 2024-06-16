from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator, Literal

import httpx
import pyarrow as pa
import pyarrow.compute as pc
from appdirs import user_cache_dir
from loguru import logger
from typing_extensions import Self

import pandas as pd

from .base import APIBase, APIRespBase, ArrowBase, HTTPClient, ServiceBase
from .common import to_unix_timestamp
from .history import (
    flight_list,
    flight_list_dict,
    playback,
    playback_metadata_dict,
    playback_track_dict,
    playback_track_ems_dict,
)
from .livefeed import livefeed_playback_world_data, livefeed_world_data
from .types.cache import (
    LiveFeedRecord,
    flight_list_schema,
    livefeed_schema,
    playback_track_schema,
)
from .types.core import (
    FlightListContext,
    LiveFeedContext,
    PlaybackContext,
)
from .types.fr24 import (
    FlightData,
    FlightList,
    Playback,
    TokenSubscriptionKey,
    UsernamePassword,
)


class FR24:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *,
        cache_dir: str = user_cache_dir("fr24"),
    ) -> None:
        """
        See docs [quickstart](../usage/quickstart.md#initialisation).

        :param client: The httpx client to use (if not provided, a new one
            will be created). It is recommended to use `http2=True`.
        :param cache_dir:
            See [cache directory](../usage/cli.md#directories).
        """
        self.http = HTTPClient(
            httpx.AsyncClient(http2=True) if client is None else client
        )
        base_dir = Path(cache_dir)
        self.flight_list = FlightListService(self.http, base_dir)
        # self.playback = PlaybackService(self.http, base_dir)
        # self.livefeed = LiveFeedService(self.http, base_dir)

    # def playback(self, flight_id: str | int) -> PlaybackService:
    #     """
    #     Constructs a [playback service][fr24.core.PlaybackService] for the
    #     given flight ID.

    #     *Related: [fr24.history.playback][]*

    #     :param flight_id: Hex Flight ID (e.g. `"2d81a27"`, `0x2d81a27`)
    #     """
    #     if not isinstance(flight_id, str):
    #         flight_id = f"{flight_id:x}"
    #     flight_id = flight_id.lower()
    #     ctx: PlaybackContext = {"flight_id": flight_id}
    #     return PlaybackService(self.http, self.cache_dir, ctx)

    # def livefeed(
    #     self,
    #     timestamp: int | str | datetime | pd.Timestamp | None = None,
    #     *,
    #     duration: int | None = None,
    #     hfreq: int | None = None,
    # ) -> LiveFeedService:
    #     """
    #     Constructs a [live feed service][fr24.core.LiveFeedService].

    #     :param timestamp: Unix timestamp (seconds) of the live feed data.
    #         If `None` the [latest live data][fr24.livefeed.livefeed_world_data]
    #         will be fetched when `.api.fetch()` is called.
    #         Otherwise,
    #         [historical data][fr24.livefeed.livefeed_playback_world_data]
    #         will be fetched instead.
    #     :param duration: Prefetch duration (default: `7` seconds). Should only
    #         be set for historical data.
    #     :param hfreq: High frequency mode (default: `0`). Should only be set for
    #         historical data.
    #     """
    #     ts = to_unix_timestamp(timestamp)
    #     if ts is None and (hfreq is not None or duration is not None):
    #         raise ValueError(
    #             "`hfreq` and `duration` can only be set for historical data."
    #         )
    #     ctx: LiveFeedContext = {
    #         "timestamp": ts,
    #         "source": "live" if ts is None else "playback",
    #         "duration": duration,
    #         "hfreq": hfreq,
    #     }
    #     return LiveFeedService(
    #         self.http,
    #         self.cache_dir,
    #         ctx,
    #     )

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

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


class FlightListAPI(APIBase[FlightListContext, FlightList]):
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


class FlightListAPIResp(APIRespBase[FlightListContext, FlightList]):
    """A wrapper around the flight list API response."""

    def to_arrow(self) -> FlightListArrow:
        """
        Parse each [fr24.types.fr24.FlightListItem][] in the API response and
        transform it into a pyarrow.Table.
        """
        flights = self.data["result"]["response"]["data"] or []
        if len(flights) == 0:
            logger.warning("no data in response, table will be empty")
        table = pa.Table.from_pylist(
            [flight_list_dict(f) for f in flights],
            schema=FlightListArrow._default_schema,
        )
        return FlightListArrow(self.ctx, table)


class FlightListArrow(ArrowBase[FlightListContext]):
    """A wrapper around a pyarrow.Table containing flight list data."""

    _default_schema: pa.Schema | None = flight_list_schema

    @classmethod
    def _fp(cls, ctx: FlightListContext) -> Path:
        return (
            ctx["base_dir"]
            / "flight_list"
            / ctx["kind"]
            / f"{ctx['ident'].upper()}.parquet"
        )

    def concat(
        self,
        data_new: ArrowBase[FlightListContext],  #  | FlightListAPIResp,
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


class FlightListService(ServiceBase[FlightListAPI, FlightListArrow]):
    """A service to handle the flight list API and file operations."""

    def __init__(
        self,
        http: HTTPClient,
        base_dir: Path,
    ) -> None:
        super().__init__(FlightListAPI(http), base_dir)

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

        *Related: [fr24.history.flight_list][]*

        Input **either** the registration or the flight number, not both.

        :param reg: Aircraft registration (e.g. `B-HUJ`)
        :param flight: Flight number (e.g. `CX8747`)
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
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
        page: int = 1,
        limit: int = 10,
        delay: int = 5,
    ) -> AsyncIterator[FlightListAPIResp]:
        """
        Iteratively fetch all pages of the flight list for the given
        registration or flight number.

        *Related: [fr24.history.flight_list][]*

        Input **either** the registration or the flight number, not both.

        :param reg: Aircraft registration (e.g. `B-HUJ`)
        :param flight: Flight number (e.g. `CX8747`)
        :param limit: Number of flights per page - use `100` if authenticated
        :param delay: Delay between requests in seconds
        """
        ctx = self._construct_ctx(reg, flight)
        async for raw in self._api._fetch_all(
            ctx, page, limit, timestamp, delay
        ):
            yield FlightListAPIResp(ctx, raw)

    def load(
        self, *, reg: str | None = None, flight: str | None = None
    ) -> FlightListArrow[FlightListContext]:
        """
        Get flight list for the given registration or flight number from
        the [cache](../usage/cli.md#directories). If the file does not exist,
        an empty table will be returned.
        """
        return FlightListArrow._load(self._construct_ctx(reg, flight))

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


# class PlaybackAPI(APIBase[Playback, PlaybackContext]):
#     async def _fetch(
#         self, timestamp: int | str | datetime | pd.Timestamp | None = None
#     ) -> Playback:
#         """
#         Fetch the historical track playback data for the given flight.

#         *Related: [fr24.history.playback][]*

#         :param timestamp: Unix timestamp (seconds) of ATD - optional, but
#             it is recommended to include it
#         """
#         return await playback(
#             self.http.client, self.ctx["flight_id"], timestamp, self.http.auth
#         )


# class PlaybackArrow(ArrowBase[Playback, PlaybackContext]):
#     """Arrow table for playback data."""

#     schema = playback_track_schema

#     @property
#     def fp(self) -> Path:
#         return self.base_dir / "playback" / f"{self.ctx['flight_id']}.parquet"

#     @staticmethod
#     def _concat(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
#         raise NotImplementedError(
#             "Cannot add data to a non-empty playback table.\n"
#             "Use `.clear()` to reset the table first."
#         )

#     def _add_api_response(self, data: Playback) -> Self:
#         """
#         Parse each [fr24.types.fr24.TrackData][] in the API response and store
#         it in the table. Also adds [fr24.types.fr24.FlightData][] into the
#         schema's metadata with key `_flight`.

#         :param data: the return data of [fr24.core.PlaybackAPI.fetch][].
#         """
#         self.schema = self.schema.with_metadata(
#             {
#                 "_flight": json.dumps(
#                     playback_metadata_dict(
#                         data["result"]["response"]["data"]["flight"]
#                     )
#                 ).encode("utf-8")
#             }
#         )
#         self.table = pa.Table.from_pylist(
#             [
#                 {
#                     **playback_track_dict(point),
#                     "ems": playback_track_ems_dict(point),
#                 }
#                 for point in data["result"]["response"]["data"]["flight"][
#                     "track"
#                 ]
#             ],
#             schema=self.schema,
#         )
#         return self

#     @property
#     def metadata(self) -> FlightData | None:
#         """Get the flight metadata from the arrow schema."""
#         if m := self.schema.metadata.get(b"_flight"):
#             return json.loads(m)  # type: ignore[no-any-return]
#         return None


# class PlaybackService(ServiceBase[PlaybackAPI, PlaybackArrow]):
#     """A service to handle the playback API and file operations."""

#     def __init__(self, http: HTTPClient, base_dir: str) -> None:
#         api = PlaybackAPI(http)
#         fs = PlaybackArrow(base_dir)
#         super().__init__(api, fs)


# class LiveFeedAPI(APIBase[list[LiveFeedRecord], LiveFeedContext]):
#     async def _fetch(self) -> list[LiveFeedRecord]:
#         """
#         Fetch the live feed data.

#         Updates `self.ctx.timestamp` to the current time if it is `None`.
#         """
#         if (ts := self.ctx["timestamp"]) is not None:
#             kw = {
#                 k: v
#                 for k, v in self.ctx.items()
#                 if k in ("duration", "hfreq") and v is not None
#             }
#             return await livefeed_playback_world_data(
#                 self.http.client,
#                 ts,
#                 **kw,  # type: ignore[arg-type]
#                 auth=self.http.auth,
#             )
#         resp = await livefeed_world_data(self.http.client, self.http.auth)
#         self.ctx["timestamp"] = int(time.time())
#         return resp


# class LiveFeedArrow(ArrowBase[list[LiveFeedRecord], LiveFeedContext]):
#     """Arrow table for live feed data."""

#     schema = livefeed_schema

#     @property
#     def fp(self) -> Path:
#         ts = self.ctx["timestamp"]
#         if self.ctx["source"] == "live" and ts is None:
#             raise ValueError(
#                 "Cannot determine file path for uninitialised live feed.\n"
#                 "Call `.api.fetch()` first to get the current timestamp."
#             )
#         return self.base_dir / "feed" / f"{ts}.parquet"

#     @staticmethod
#     def _concat(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
#         raise NotImplementedError(
#             "Cannot add data to a non-empty live feed table.\n"
#             "Use `.clear()` to reset the table first."
#         )

#     def _add_api_response(self, data: list[LiveFeedRecord]) -> Self:
#         """
#         Parse each [fr24.types.cache.LiveFeedRecord][] in the API response and
#         store it in the table.

#         :param data: the return data of [fr24.core.LiveFeedAPI.fetch][].
#         """
#         self.schema = self.schema.with_metadata(
#             {"ctx": json.dumps(self.ctx).encode("utf-8")}
#         )
#         self.table = pa.Table.from_pylist(data, schema=self.schema)
#         return self


# class LiveFeedService(ServiceBase[LiveFeedAPI, LiveFeedArrow]):
#     """A service to handle the live feed API and file operations."""

#     def __init__(self, http: HTTPClient, base_dir: str) -> None:
#         api = LiveFeedAPI(http)
#         fs = LiveFeedArrow(base_dir)
#         super().__init__(api, fs)
