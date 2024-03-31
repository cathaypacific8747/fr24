from __future__ import annotations

import asyncio
import json

# import time
import warnings
from datetime import datetime

# from pathlib import Path
from typing import Any, AsyncIterator

import pyarrow as pa
import pyarrow.compute as pc

# import pyarrow.parquet as pq
from appdirs import user_cache_dir
from loguru import logger
from typing_extensions import Self

import pandas as pd

from .base import APIBase, ArrowBase, HTTPClient, ServiceBase
from .history import (
    flight_list,
    flight_list_dict,
    playback,
    playback_metadata_dict,
    playback_track_dict,
    playback_track_ems_dict,
)

# from .livefeed import livefeed_playback_world_data, livefeed_world_data
from .types.cache import (
    flight_list_schema,
    playback_track_schema,
)

# livefeed_schema,
from .types.fr24 import FlightData, FlightList, Playback


class FlightListAPI(APIBase[FlightList]):
    def __init__(
        self, http: HTTPClient, reg: str | None, flight: str | None
    ) -> None:
        super().__init__(http)
        self.reg = reg
        self.flight = flight

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
            self.reg,
            self.flight,
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


class FlightListArrow(ArrowBase[FlightList]):
    """Arrow table for flight list data."""

    schema = flight_list_schema

    def __init__(
        self,
        base_dir: str,
        reg: str | None,
        flight: str | None,
    ) -> None:
        super().__init__(base_dir)
        foln, fln = (
            ("reg", reg.upper())
            if reg is not None
            else ("flight", flight.upper())  # type: ignore[union-attr]
        )
        self.fp = self.base_dir / "flight_list" / foln / f"{fln}.parquet"

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


class FlightListService(ServiceBase[FlightListAPI, FlightListArrow]):
    """A service to handle the flight list API and file operations."""

    def __init__(
        self,
        http: HTTPClient,
        base_dir: str,
        reg: str | None,
        flight: str | None,
    ) -> None:
        api = FlightListAPI(http, reg, flight)
        fs = FlightListArrow(base_dir, reg, flight)
        super().__init__(api, fs)
        self.reg = reg
        self.flight = flight


class PlaybackAPI(APIBase[Playback]):
    def __init__(self, http: HTTPClient, flight_id: str) -> None:
        super().__init__(http)
        self.flight_id = flight_id

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
            self.http.client, self.flight_id, timestamp, self.http.auth
        )


class PlaybackArrow(ArrowBase[Playback]):
    """Arrow table for playback data."""

    schema = playback_track_schema

    def __init__(self, base_dir: str, flight_id: str) -> None:
        super().__init__(base_dir)
        self.fp = self.base_dir / "playback" / f"{flight_id}.parquet"

    @staticmethod
    def _concat_tables(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
        raise RuntimeError(
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


class PlaybackService(ServiceBase[PlaybackAPI, PlaybackArrow]):
    """A service to handle the playback API and file operations."""

    def __init__(self, http: HTTPClient, base_dir: str, flight_id: str) -> None:
        api = PlaybackAPI(http, flight_id)
        fs = PlaybackArrow(base_dir, flight_id)
        super().__init__(api, fs)
        self.flight_id = flight_id


class FR24:
    def __init__(self, cache_dir: str = user_cache_dir("fr24")) -> None:
        """
        Populate http clients cache for each service.

        Check the [cache directory](/usage/cli/#directories) for more details.
        """
        self.http = HTTPClient()
        self.cache_dir = cache_dir

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)

    def flight_list(
        self, /, reg: str | None = None, flight: str | None = None
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
        return FlightListService(self.http, self.cache_dir, reg, flight)

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
        return PlaybackService(self.http, self.cache_dir, flight_id)

    async def cache_livefeed_playback_world_insert(
        self, timestamp: int, duration: int = 7, hfreq: int = 0
    ) -> None:
        """
        [DEPRECATED]
        Request playback of live feed and save to the cache directory
        """
        self._warn_deprecated()

        # data = await livefeed_playback_world_data(
        #     self.client, timestamp, duration, hfreq, self.auth
        # )

        # fp = (
        #     self.cache_dir
        #     / "feed"
        #     / "playback"
        #     / f"{timestamp * 1000:.0f}_{duration:.0f}.parquet"
        # )
        # pq.write_table(pa.Table.from_pylist(data, schema=livefeed_schema), fp)
        # return fp

    async def cache_livefeed(self) -> None:
        """[DEPRECATED] Request live feed and save to the cache directory."""
        self._warn_deprecated()
        # data = await livefeed_world_data(self.client, self.auth)

        # fp = (
        #     self.cache_dir
        #     / "feed"
        #     / "live"
        #     / f"{time.time() * 1000:.0f}.parquet"
        # )
        # pq.write_table(pa.Table.from_pylist(data, schema=livefeed_schema), fp)
        # return fp

    def _warn_deprecated(self) -> None:
        warnings.warn(
            "This method is deprecated to accomodate for the new core.",
            DeprecationWarning,
        )
