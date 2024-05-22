from copy import deepcopy

import pytest
from fr24.core import FR24


@pytest.mark.asyncio
async def test_flight_list_single() -> None:
    async with FR24() as fr24:
        with pytest.raises(ValueError):  # missing reg/flight
            _ = await fr24.flight_list.fetch()
        response = await fr24.flight_list.fetch(reg="b-hpb")
        assert response.data["result"]["response"]["data"] is not None

        assert response.to_arrow().table.num_rows > 5


@pytest.mark.asyncio
async def test_flight_list_paginate() -> None:
    """
    call 2 rows in 3 pages, combining them should yield 6 rows
    """
    async with FR24() as fr24:
        fl = fr24.flight_list(reg="b-hpb")

        i = 0
        num_rows = 0
        async for response in fl.api.fetch_all(limit=2):
            assert response["result"]["response"]["data"] is not None

            fl.data._add_api_response(response)
            assert fl.data.table is not None
            assert fl.data.table.num_rows > num_rows
            assert num_rows == i * 2  # shouldn't fail, but just in case
            num_rows = fl.data.table.num_rows
            if num_rows >= 6:
                break
            i += 1


@pytest.mark.asyncio
async def test_flight_list_overlapping() -> None:
    """
    if we have existing flightids (10, 9, 8, 7) + new flightids (8, 7, 6, 5),
    the union of them should result in (10, 9, 8, 7, 6, 5)
    """
    async with FR24() as fr24:
        # add existing data
        fl = fr24.flight_list(reg="b-hpb")

        response = await fl.api._fetch(limit=6)
        flights = response["result"]["response"]["data"]
        assert flights is not None
        assert len(flights) == 6

        response0 = deepcopy(response)
        response0["result"]["response"]["data"] = flights[:4]
        response1 = deepcopy(response)
        response1["result"]["response"]["data"] = flights[2:]

        fl.data._add_api_response(response0)
        assert fl.data.df is not None
        assert fl.data.df.shape[0] == 4
        fl.data._add_api_response(response1)
        assert fl.data.df is not None
        assert fl.data.df.shape[0] == 6


@pytest.mark.asyncio
async def test_flight_list_file_ops() -> None:
    """
    check that saving and reopening in a new instance yields the same rows
    """
    async with FR24() as fr24:
        response = await fr24.flight_list.fetch(reg="b-hpb")

        # fl = fr24.flight_list(reg="b-hPb")

        # # make directories and delete files if it exists
        # fl.data.fp.parent.mkdir(parents=True, exist_ok=True)
        # fl.data.fp.unlink(missing_ok=True)
        # fl.data._add_api_response(await fl.api._fetch(limit=3))
        # assert fl.data.table is not None

        # fl.data._save_parquet()
        # assert fl.data.fp.stem == "B-HPB"
        # assert fl.data.fp.exists()

        # fl2 = fr24.flight_list(reg="b-hpb")
        # fl2.data._add_parquet()

        # assert fl2.data.table is not None
        # assert fl.data.table.equals(fl2.data.table)
