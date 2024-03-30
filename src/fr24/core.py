from __future__ import annotations

import asyncio

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
)

# playback,
# playback_metadata_dict,
# playback_track_dict,
# playback_track_ems_dict,
# from .livefeed import livefeed_playback_world_data, livefeed_world_data
from .types.cache import (
    flight_list_schema,
)

# livefeed_schema,
# playback_track_ems_schema,
# playback_track_schema,
from .types.fr24 import FlightList


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
    """A wrapper around the Arrow table holding flight list data."""

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
        Parse the API response into the table.

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

    async def cache_playback_upsert(
        self,
        flight_id: int | str,
        timestamp: int | str | datetime | pd.Timestamp | None = None,
        overwrite: bool = False,
    ) -> None:
        """
        [DEPRECATED]
        Attempt to read the metadata cache, if it doesn't exist, create
         `{metadata & track & track_ems}/{id}.parquet`
        """
        self._warn_deprecated()
        # if not isinstance(flight_id, str):
        #     flight_id = f"{flight_id:x}"
        # flight_id = flight_id.lower()

        # rootdir = self.cache_dir / "playback"
        # fp_metadata = rootdir / "metadata" / f"{flight_id}.parquet"
        # fp_track = rootdir / "track" / f"{flight_id}.parquet"
        # fp_track_ems = rootdir / "track_ems" / f"{flight_id}.parquet"
        # if not overwrite and fp_metadata.exists():
        #     return fp_metadata

        # pb = await playback(self.client, flight_id, timestamp, self.auth)
        # track, track_ems = [], []
        # for point in pb["result"]["response"]["data"]["flight"]["track"]:
        #     track.append(playback_track_dict(point))
        #     if (e := playback_track_ems_dict(point)) is not None:
        #         track_ems.append(e)

        # # TODO: combine all metadata into single parquet
        # meta_table = pa.Table.from_pylist(
        #     [playback_metadata_dict(
        #         pb["result"]["response"]["data"]["flight"]
        #     )]
        # )
        # with pq.ParquetWriter(fp_metadata, meta_table.schema) as writer:
        #     writer.write_table(meta_table)
        # with pq.ParquetWriter(fp_track, playback_track_schema) as writer:
        #     writer.write_table(
        #         pa.Table.from_pylist(track, schema=playback_track_schema)
        #     )
        # with pq.ParquetWriter(
        #     fp_track_ems, playback_track_ems_schema
        # ) as writer:
        #     writer.write_table(
        #         pa.Table.from_pylist(
        #             track_ems,
        #             schema=playback_track_ems_schema,
        #         )
        #     )

        # return fp_metadata

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
