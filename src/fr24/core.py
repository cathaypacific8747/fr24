from __future__ import annotations

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
from appdirs import user_cache_dir
from loguru import logger
from typing_extensions import Self

import numpy as np
import numpy.typing as npt
import pandas as pd

from .authentication import login
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
    flight_list_schema,
    livefeed_schema,
    playback_track_ems_schema,
    playback_track_schema,
)
from .types.fr24 import Authentication, FlightList


class FR24:
    def __init__(self, cache_dir: str = user_cache_dir("fr24")) -> None:
        """
        Populate http clients and build the cache directory tree.

        Check the [cache directory](/usage/cli/#directories) for more details.
        """
        self.client = httpx.AsyncClient()
        self.auth: Authentication | None = None
        self.cache_dir = Path(cache_dir)
        for d in (
            self.cache_dir,
            self.cache_dir / "flight_list" / "reg",
            self.cache_dir / "flight_list" / "flight",
            self.cache_dir / "playback" / "metadata",
            self.cache_dir / "playback" / "track",
            self.cache_dir / "playback" / "track_ems",
            self.cache_dir / "feed" / "playback",
            self.cache_dir / "feed" / "live",
        ):
            d.mkdir(parents=True, exist_ok=True)

    async def __aenter__(self) -> Self:
        self.auth = await login(self.client)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self.client is not None:
            await self.client.aclose()

    async def _flight_list_iter(
        self,
        reg: None | str = None,
        flight: None | str = None,
        page: int = 1,
        limit: int = 100,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
    ) -> AsyncIterator[FlightList]:
        """
        Yield each page in the flight list API, retrying up to 3 times
        with 2s delay.
        """
        more = True
        while more:
            for rt in range(3):
                try:
                    fl = await flight_list(
                        self.client,
                        reg,
                        flight,
                        page,
                        limit,
                        timestamp,
                        self.auth,
                    )
                    yield fl
                    break
                except httpx.HTTPStatusError as e:
                    logger.warning(f"[{e.response.status_code}] retry {rt}")
                    await asyncio.sleep(5 * rt)
            else:
                logger.error(f"Failed to download {reg=} {flight=}")
                break

            # NOTE: both page+ts needs to be updated for the next request
            if (data := fl["result"]["response"]["data"]) is None:
                break
            timestamp = min(
                d["time"]["scheduled"]["departure"]
                for d in data
                if d["time"]["scheduled"]["departure"] is not None
            )
            page += 1
            more = fl["result"]["response"]["page"]["more"]
            await asyncio.sleep(2)

    async def cache_flight_list_upsert(
        self,
        reg: None | str = None,
        flight: None | str = None,
        page: int = 1,
        limit: int = 100,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
        overwrite: bool = False,
    ) -> Path:
        """
        Iteratively update the cache by querying in batches,
        whenever a duplicate is found in that batch, stop querying.

        The "Estimated XX:XX" status will also be updated to the latest.
        """
        foln, fn = (
            ("flight", str(flight).upper())
            if reg is None
            else ("reg", str(reg).upper())
        )
        cache_fp = self.cache_dir / "flight_list" / foln / f"{fn}.parquet"

        tbl_old: pa.Table | None = None
        existing_fids = []
        existing_mask: npt.NDArray[np.bool_] = np.array([], dtype=np.bool_)
        if not overwrite and cache_fp.exists():
            tbl_old = pq.read_table(str(cache_fp), schema=flight_list_schema)
            existing_fids = tbl_old["flight_id"].to_pylist()
            existing_mask = np.full(len(tbl_old), False)

        found_duplicate = False
        fl_rec_new = []
        async for batch in self._flight_list_iter(
            reg, flight, page, limit, timestamp
        ):
            for entry in batch["result"]["response"]["data"] or []:
                d = flight_list_dict(entry)
                fl_rec_new.append(d)
                if d["flight_id"] in existing_fids:
                    existing_mask[existing_fids.index(d["flight_id"])] = True
                    found_duplicate = True
            logger.debug(f"{len(fl_rec_new)=} {found_duplicate=}")
            if found_duplicate:
                break
        tbl_new = pa.Table.from_pylist(
            fl_rec_new, # type: ignore
            schema=flight_list_schema,
        )
        if found_duplicate:
            tbl_new = pa.concat_tables(
                [
                    tbl_new,
                    tbl_old.filter(pa.array(~existing_mask)),  # type: ignore
                ]
            )
        with pq.ParquetWriter(cache_fp, flight_list_schema) as writer:
            writer.write_table(tbl_new)
        return cache_fp

    async def cache_playback_upsert(
        self,
        flight_id: int | str,
        timestamp: int | str | datetime | pd.Timestamp | None = None,
        overwrite: bool = False,
    ) -> Path:
        """
        Attempt to read the metadata cache, if it doesn't exist, create
         `{metadata & track & track_ems}/{id}.parquet`
        """
        if not isinstance(flight_id, str):
            flight_id = f"{flight_id:x}"
        flight_id = flight_id.lower()

        rootdir = self.cache_dir / "playback"
        fp_metadata = rootdir / "metadata" / f"{flight_id}.parquet"
        fp_track = rootdir / "track" / f"{flight_id}.parquet"
        fp_track_ems = rootdir / "track_ems" / f"{flight_id}.parquet"
        if not overwrite and fp_metadata.exists():
            return fp_metadata

        pb = await playback(self.client, flight_id, timestamp, self.auth)
        track, track_ems = [], []
        for point in pb["result"]["response"]["data"]["flight"]["track"]:
            track.append(playback_track_dict(point))
            if (e := playback_track_ems_dict(point)) is not None:
                track_ems.append(e)

        # TODO: combine all metadata into single parquet
        meta_table = pa.Table.from_pylist(
            [playback_metadata_dict(pb["result"]["response"]["data"]["flight"])]
        )
        with pq.ParquetWriter(fp_metadata, meta_table.schema) as writer:
            writer.write_table(meta_table)
        with pq.ParquetWriter(fp_track, playback_track_schema) as writer:
            writer.write_table(
                pa.Table.from_pylist(track, schema=playback_track_schema) # type: ignore
            )
        with pq.ParquetWriter(
            fp_track_ems, playback_track_ems_schema
        ) as writer:
            writer.write_table(
                pa.Table.from_pylist(
                    track_ems, schema=playback_track_ems_schema # type: ignore
                )
            )

        return fp_metadata

    async def cache_livefeed_playback_world_insert(
        self, timestamp: int, duration: int = 7, hfreq: int = 0
    ) -> Path:
        """Request playback of live feed and save to the cache directory"""
        data = await livefeed_playback_world_data(
            self.client, timestamp, duration, hfreq, self.auth
        )

        fp = (
            self.cache_dir
            / "feed"
            / "playback"
            / f"{timestamp * 1000:.0f}_{duration:.0f}.parquet"
        )
        pq.write_table(pa.Table.from_pylist(data, schema=livefeed_schema), fp) # type: ignore
        return fp

    async def cache_livefeed(self) -> Path:
        """Request live feed and save to the cache directory."""
        data = await livefeed_world_data(self.client, self.auth)

        fp = (
            self.cache_dir
            / "feed"
            / "live"
            / f"{time.time() * 1000:.0f}.parquet"
        )
        pq.write_table(pa.Table.from_pylist(data, schema=livefeed_schema), fp) # type: ignore
        return fp
