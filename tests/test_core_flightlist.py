from copy import deepcopy
from pathlib import Path
from typing import Callable

import pyarrow.parquet as pq
import pytest
from fr24.core import FR24, FlightListArrow

REG = "b-hpb"


@pytest.mark.asyncio
async def test_flight_list_single() -> None:
    async with FR24() as fr24:
        with pytest.raises(ValueError):  # missing reg/flight
            _ = await fr24.flight_list.fetch()
        response = await fr24.flight_list.fetch(reg=REG)
        assert response.data["result"]["response"]["data"] is not None

        datac = response.to_arrow()
        assert datac.data.num_rows > 5
        # make sure pandas df shape is same as arrow table
        assert datac.df.shape[0] == datac.data.num_rows
        assert datac.df.shape[1] == datac.data.num_columns


@pytest.mark.asyncio
async def test_flight_list_paginate() -> None:
    """
    call 2 rows in 3 pages, combining them should yield 6 rows
    """
    async with FR24() as fr24:
        datac = fr24.flight_list.load(reg=REG)
        assert datac.data.num_rows == 0

        i = 0
        async for resp in fr24.flight_list.fetch_all(reg=REG, limit=2, delay=5):
            assert resp.data["result"]["response"]["data"] is not None
            datac_new = resp.to_arrow()
            assert datac_new.data.num_rows > 0
            curr_rows = datac.data.num_rows
            assert curr_rows == i * 2

            datac.concat(datac_new, inplace=True)
            assert datac.data.num_rows == curr_rows + 2
            if datac.data.num_rows >= 6:
                break
            if i > 5:
                break  # safety net in case of infinite loop
            i += 1


@pytest.mark.asyncio
async def test_flight_list_concat() -> None:
    """
    if we have existing flightids (10, 9, 8, 7) + new flightids (8, 7, 6, 5),
    the union of them should result in (10, 9, 8, 7, 6, 5)
    """
    async with FR24() as fr24:
        response = await fr24.flight_list.fetch(reg=REG, limit=6)
        flights = response.data["result"]["response"]["data"]
        assert flights is not None
        assert len(flights) == 6

        response0 = deepcopy(response)
        response0.data["result"]["response"]["data"] = flights[:4]
        response1 = deepcopy(response)
        response1.data["result"]["response"]["data"] = flights[2:]

        datac = fr24.flight_list.load(reg=REG)
        datac.concat(response0.to_arrow(), inplace=True)
        assert datac.data.num_rows == 4
        datac.concat(response1.to_arrow(), inplace=True)
        assert datac.data.num_rows == 6


@pytest.mark.asyncio
async def test_flight_list_file_ops() -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    test that auto-detect directory and specified directory saving works
    """
    async with FR24() as fr24:
        response = await fr24.flight_list.fetch(reg=REG)

        datac = response.to_arrow()
        curr_rows = datac.data.num_rows

        def test_ok(fp: Path, cb: Callable[[], FlightListArrow]) -> None:
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.unlink(missing_ok=True)
            _ = cb()
            assert fp.exists()
            table = pq.read_table(fp)
            assert table.num_rows == curr_rows
            fp.unlink()

        specific_fp = Path(__file__).parent / "tmp" / "test.parquet"
        test_ok(specific_fp, lambda: datac.save(specific_fp))
        specific_fp.parent.rmdir()

        test_ok(
            fr24.base_dir / "flight_list" / "reg" / f"{REG.upper()}.parquet",
            lambda: datac.save(),
        )
