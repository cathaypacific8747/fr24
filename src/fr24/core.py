from __future__ import annotations

import asyncio
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
import pyarrow as pa
import pyarrow.compute as pc
from appdirs import user_cache_dir
from loguru import logger
from typing_extensions import Self

import pandas as pd

from .base import APIBase, ArrowBase, HTTPClient, ServiceBase
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
from .types.core import FlightListContext, LiveFeedContext, PlaybackContext
from .types.fr24 import (
    FlightData,
    FlightList,
    Playback,
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
            will be created).
        :param cache_dir:
            See [cache directory](../usage/cli.md#directories).
        """
        self.http = HTTPClient(
            httpx.AsyncClient() if client is None else client
        )
        self.cache_dir = cache_dir

    def flight_list(
        self, *, reg: str | None = None, flight: str | None = None
    ) -> FlightListService:
        """
        Constructs a [flight list service][fr24.core.FlightListService] for the
        given registration or flight number.

        *Related: [fr24.history.flight_list][]*

        Input **either** the registration or the flight number, not both.

        :param reg: Aircraft registration (e.g. `B-HUJ`)
        :param flight: Flight number (e.g. `CX8747`)
        """
        if not ((reg is None) ^ (flight is None)):
            raise ValueError(
                "Either reg or flight must be provided, not both or neither."
            )
        ctx: FlightListContext = {"reg": reg, "flight": flight}
        return FlightListService(self.http, self.cache_dir, ctx)

    def playback(self, flight_id: str | int) -> PlaybackService:
        """
        Constructs a [playback service][fr24.core.PlaybackService] for the
        given flight ID.

        *Related: [fr24.history.playback][]*

        :param flight_id: Hex Flight ID (e.g. `"2d81a27"`, `0x2d81a27`)
        """
        if not isinstance(flight_id, str):
            flight_id = f"{flight_id:x}"
        flight_id = flight_id.lower()
        ctx: PlaybackContext = {"flight_id": flight_id}
        return PlaybackService(self.http, self.cache_dir, ctx)

    def livefeed(
        self,
        timestamp: int | str | datetime | pd.Timestamp | None = None,
        *,
        duration: int | None = None,
        hfreq: int | None = None,
    ) -> LiveFeedService:
        """
        Constructs a [live feed service][fr24.core.LiveFeedService].

        :param timestamp: Unix timestamp (seconds) of the live feed data.
            If `None` the [latest live data][fr24.livefeed.livefeed_world_data]
            will be fetched when `.api.fetch()` is called.
            Otherwise,
            [historical data][fr24.livefeed.livefeed_playback_world_data]
            will be fetched instead.
        :param duration: Prefetch duration (default: `7` seconds). Should only
            be set for historical data.
        :param hfreq: High frequency mode (default: `0`). Should only be set for
            historical data.
        """
        ts = to_unix_timestamp(timestamp)
        if ts is None and (hfreq is not None or duration is not None):
            raise ValueError(
                "`hfreq` and `duration` can only be set for historical data."
            )
        ctx: LiveFeedContext = {
            "timestamp": ts,
            "source": "live" if ts is None else "playback",
            "duration": duration,
            "hfreq": hfreq,
        }
        return LiveFeedService(
            self.http,
            self.cache_dir,
            ctx,
        )

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


class FlightListAPI(APIBase[FlightList, FlightListContext]):
    async def fetch(
        self,
        page: int = 1,
        limit: int = 10,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
    ) -> FlightList:
        """
        Fetch one page of flight list.

        *Related: [fr24.history.flight_list][]*
        """
        return await flight_list(
            self.http.client,
            self.ctx["reg"],
            self.ctx["flight"],
            page,
            limit,
            timestamp,
            self.http.auth,
        )

    async def fetch_all(
        self,
        page: int = 1,
        limit: int = 10,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
        delay: int = 1,
    ) -> AsyncIterator[FlightList]:
        """
        Iteratively fetch all pages of the flight list.

        *Related: [fr24.history.flight_list][]*

        :param delay: Delay between requests in seconds
        """
        more = True
        while more:
            fl = await self.fetch(page, limit, timestamp)

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


class FlightListArrow(ArrowBase[FlightList, FlightListContext]):
    """Arrow table for flight list data."""

    schema = flight_list_schema

    @property
    def fp(self) -> Path:
        if self.ctx["reg"] is not None:
            return (
                self.base_dir
                / "flight_list"
                / "reg"
                / f"{self.ctx['reg'].upper()}.parquet"
            )
        elif self.ctx["flight"] is not None:
            return (
                self.base_dir
                / "flight_list"
                / "flight"
                / f"{self.ctx['flight'].upper()}.parquet"
            )
        raise ValueError("Both reg and flight are None.")

    @staticmethod
    def _concat_tables(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
        """
        Combine old and new flights, removing duplicates in the old table.

        This should in turn update all aircraft with the "Estimated" status
        with the new data.
        """
        mask: pa.ChunkedArray = pc.is_in(
            tbl_old["flight_id"], value_set=tbl_new["flight_id"]
        )
        if (dup_count := pc.sum(mask).as_py()) > 0:
            logger.warning(f"overwriting {dup_count} duplicate flight ids.")
        return pa.concat_tables(
            [tbl_old.filter(pc.invert(mask.combine_chunks())), tbl_new]
        )

    def add_api_response(self, data: FlightList) -> Self:
        """
        Parse each [fr24.types.fr24.FlightListItem][] in the API response and
        store it in the table.

        :param data: the return data of [fr24.core.FlightListAPI.fetch][].
        """
        if flights := data["result"]["response"]["data"]:
            self.table = pa.Table.from_pylist(
                [flight_list_dict(f) for f in flights],
                schema=self.schema,
            )
        else:
            logger.warning("No data in the API response.")
        return self


class FlightListService(
    ServiceBase[FlightListAPI, FlightListArrow, FlightListContext]
):
    """A service to handle the flight list API and file operations."""

    def __init__(
        self,
        http: HTTPClient,
        base_dir: str,
        ctx: FlightListContext,
    ) -> None:
        api = FlightListAPI(http, ctx)
        fs = FlightListArrow(base_dir, ctx)
        super().__init__(api, fs, ctx)


class PlaybackAPI(APIBase[Playback, PlaybackContext]):
    async def fetch(
        self, timestamp: int | str | datetime | pd.Timestamp | None = None
    ) -> Playback:
        """
        Fetch the historical track playback data for the given flight.

        *Related: [fr24.history.playback][]*

        :param timestamp: Unix timestamp (seconds) of ATD - optional, but
            it is recommended to include it
        """
        return await playback(
            self.http.client, self.ctx["flight_id"], timestamp, self.http.auth
        )


class PlaybackArrow(ArrowBase[Playback, PlaybackContext]):
    """Arrow table for playback data."""

    schema = playback_track_schema

    @property
    def fp(self) -> Path:
        return self.base_dir / "playback" / f"{self.ctx['flight_id']}.parquet"

    @staticmethod
    def _concat_tables(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
        raise NotImplementedError(
            "Cannot add data to a non-empty playback table.\n"
            "Use `.clear()` to reset the table first."
        )

    def add_api_response(self, data: Playback) -> Self:
        """
        Parse each [fr24.types.fr24.TrackData][] in the API response and store
        it in the table. Also adds [fr24.types.fr24.FlightData][] into the
        schema's metadata with key `_flight`.

        :param data: the return data of [fr24.core.PlaybackAPI.fetch][].
        """
        self.schema = self.schema.with_metadata(
            {
                "_flight": json.dumps(
                    playback_metadata_dict(
                        data["result"]["response"]["data"]["flight"]
                    )
                ).encode("utf-8")
            }
        )
        self.table = pa.Table.from_pylist(
            [
                {
                    **playback_track_dict(point),
                    "ems": playback_track_ems_dict(point),
                }
                for point in data["result"]["response"]["data"]["flight"][
                    "track"
                ]
            ],
            schema=self.schema,
        )
        return self

    @property
    def metadata(self) -> FlightData | None:
        """Get the flight metadata from the arrow schema."""
        if m := self.schema.metadata.get(b"_flight"):
            return json.loads(m)  # type: ignore[no-any-return]
        return None


class PlaybackService(ServiceBase[PlaybackAPI, PlaybackArrow, PlaybackContext]):
    """A service to handle the playback API and file operations."""

    def __init__(
        self, http: HTTPClient, base_dir: str, ctx: PlaybackContext
    ) -> None:
        api = PlaybackAPI(http, ctx)
        fs = PlaybackArrow(base_dir, ctx)
        super().__init__(api, fs, ctx)


class LiveFeedAPI(APIBase[list[LiveFeedRecord], LiveFeedContext]):
    async def fetch(self) -> list[LiveFeedRecord]:
        """
        Fetch the live feed data.

        Updates `self.ctx.timestamp` to the current time if it is `None`.
        """
        if (ts := self.ctx["timestamp"]) is not None:
            kw = {
                k: v
                for k, v in self.ctx.items()
                if k in ("duration", "hfreq") and v is not None
            }
            return await livefeed_playback_world_data(
                self.http.client,
                ts,
                **kw,  # type: ignore[arg-type]
                auth=self.http.auth,
            )
        resp = await livefeed_world_data(self.http.client, self.http.auth)
        self.ctx["timestamp"] = int(time.time())
        return resp


class LiveFeedArrow(ArrowBase[list[LiveFeedRecord], LiveFeedContext]):
    """Arrow table for live feed data."""

    schema = livefeed_schema

    @property
    def fp(self) -> Path:
        ts = self.ctx["timestamp"]
        if self.ctx["source"] == "live" and ts is None:
            raise ValueError(
                "Cannot determine file path for uninitialised live feed.\n"
                "Call `.api.fetch()` first to get the current timestamp."
            )
        return self.base_dir / "feed" / f"{ts}.parquet"

    @staticmethod
    def _concat_tables(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
        raise NotImplementedError(
            "Cannot add data to a non-empty live feed table.\n"
            "Use `.clear()` to reset the table first."
        )

    def add_api_response(self, data: list[LiveFeedRecord]) -> Self:
        """
        Parse each [fr24.types.cache.LiveFeedRecord][] in the API response and
        store it in the table.

        :param data: the return data of [fr24.core.LiveFeedAPI.fetch][].
        """
        self.schema = self.schema.with_metadata(
            {"ctx": json.dumps(self.ctx).encode("utf-8")}
        )
        self.table = pa.Table.from_pylist(data, schema=self.schema)
        return self


class LiveFeedService(ServiceBase[LiveFeedAPI, LiveFeedArrow, LiveFeedContext]):
    """A service to handle the live feed API and file operations."""

    def __init__(
        self, http: HTTPClient, base_dir: str, ctx: LiveFeedContext
    ) -> None:
        api = LiveFeedAPI(http, ctx)
        fs = LiveFeedArrow(base_dir, ctx)
        super().__init__(api, fs, ctx)
