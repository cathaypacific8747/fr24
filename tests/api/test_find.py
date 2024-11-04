import httpx
import pytest
from pydantic import BaseModel, Discriminator
from typing_extensions import Annotated

from fr24.json import find
from fr24.types.find import (
    Entry,
    Stats,
    is_aircraft,
    is_airport,
    is_live,
    is_operator,
    is_schedule,
)


# overwriting the original FindResult for now
# https://github.com/python/typing/issues/1467
class FindResult(BaseModel):
    results: list[Annotated[Entry, Discriminator("type")]]
    stats: Stats


# search terms are intentionally ambiguous for larger results


@pytest.mark.asyncio
async def test_find_airport() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "tou")
        assert list_ is not None
        assert list_["stats"]["count"]["airport"] >= 2

        found_francazal = False
        for result in list_["results"]:
            assert is_airport(result)
            if "LFBF" in result["label"]:
                found_francazal = True
        assert found_francazal

        FindResult.model_validate(list_)


@pytest.mark.asyncio
async def test_find_aircraft() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "b-hp")
        assert list_ is not None

        found_bhpb = False
        for result in list_["results"]:
            if is_aircraft(result) and result["id"] == "B-HPB":
                found_bhpb = True

        assert found_bhpb

        FindResult.model_validate(list_)


@pytest.mark.asyncio
async def test_find_operator() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "cat")
        assert list_ is not None

        found_cathay = False
        for result in list_["results"]:
            if is_operator(result) and "Cathay" in result["label"]:
                found_cathay = True
        assert found_cathay

        FindResult.model_validate(list_)


@pytest.mark.asyncio
async def test_find_schedule_and_live() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "hkg-tpe")
        assert list_ is not None

        schedule_count = 0
        live_count = 0
        for result in list_["results"]:
            if is_schedule(result):
                schedule_count += 1
            elif is_live(result):
                live_count += 1
        assert list_["stats"]["count"]["schedule"] == schedule_count
        assert schedule_count > 0
        assert list_["stats"]["count"]["live"] == live_count
        assert live_count > 0

        FindResult.model_validate(list_)
