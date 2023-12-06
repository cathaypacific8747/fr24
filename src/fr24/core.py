from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import AsyncIterator

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
from .history import flight_list, flight_list_dict
from .types.cache import flight_list_schema
from .types.fr24 import Authentication, FlightList

CACHE_DIR = Path(user_cache_dir("fr24"))

for d in (
    CACHE_DIR,
    CACHE_DIR / "flight_list",
    CACHE_DIR / "flight_list" / "reg",
    CACHE_DIR / "flight_list" / "flight",
):
    d.mkdir(parents=True, exist_ok=True)


class FR24:
    def __init__(self) -> None:
        self.client = httpx.AsyncClient()
        self.auth: Authentication | None = None

    async def __aenter__(self) -> Self:
        self.auth = await login(self.client)
        return self

    async def __aexit__(self) -> None:
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
        more = True
        while more:
            for retries in range(3):
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
                except httpx.HTTPStatusError:
                    retries += 1
                    logger.warning(f"[retry {retries}] 402, backing off")
                    await asyncio.sleep(5 * retries)
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
            await asyncio.sleep(2)  # TODO: use aiometer instead

    async def flight_list_cache_update(
        self,
        reg: None | str = None,
        flight: None | str = None,
        page: int = 1,
        limit: int = 100,
        timestamp: int | datetime | pd.Timestamp | str | None = "now",
        overwrite: bool = False,
    ) -> Path:
        # attempt to update the cache by querying in batches,
        # whenever a duplicate is found in that batch, stop querying.
        # this should also update the "Estimated XX:XX" status to the latest
        foln, fn = (
            ("flight", str(flight).upper())
            if reg is None
            else ("reg", str(reg).upper())
        )
        cache_fp = CACHE_DIR / "flight_list" / foln / f"{fn}.parquet"

        tbl_old: pa.Table | None = None
        existing_fids = []
        existing_mask: npt.NDArray[np.bool_] = np.array([], dtype=np.bool_)
        if not overwrite and cache_fp.exists():
            tbl_old = pq.read_table(cache_fp, schema=flight_list_schema)
            existing_fids = tbl_old["flight_id"].to_pylist()
            existing_mask = np.full(len(tbl_old), False)

        with pq.ParquetWriter(cache_fp, flight_list_schema) as writer:
            found_duplicate = False
            fl_rec_new = []
            async for batch in self._flight_list_iter(
                reg, flight, page, limit, timestamp
            ):
                for entry in batch["result"]["response"]["data"] or []:
                    d = flight_list_dict(entry)
                    fl_rec_new.append(d)
                    if d["flight_id"] in existing_fids:
                        existing_mask[
                            existing_fids.index(d["flight_id"])
                        ] = True
                        found_duplicate = True
                logger.debug(f"{len(fl_rec_new)=} {found_duplicate=}")
                if found_duplicate:
                    break
            tbl_new = pa.Table.from_pylist(
                fl_rec_new,
                schema=flight_list_schema,
            )
            if found_duplicate:
                tbl_new = pa.concat_tables(
                    [
                        tbl_new,
                        tbl_old.filter(pa.array(~existing_mask)),  # type: ignore
                    ]
                )
            writer.write_table(tbl_new)
        return cache_fp
