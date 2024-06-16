import asyncio
import time

import httpx
import pytest
from fr24.find import find
from fr24.history import flight_list, flight_list_df, playback
from fr24.livefeed import (
    livefeed_message_create,
    livefeed_playback_world_data,
    livefeed_post,
    livefeed_request_create,
    livefeed_response_parse,
    livefeed_world_data,
)
from google.protobuf.json_format import MessageToDict


@pytest.mark.asyncio
async def test_simple() -> None:
    message = livefeed_message_create(north=50, west=-7, south=40, east=10)
    request = livefeed_request_create(message)
    async with httpx.AsyncClient() as client:
        data = await livefeed_post(client, request)
        result = livefeed_response_parse(data)
        assert result is not None

        json_output = MessageToDict(
            result,
            use_integers_for_enums=False,
            preserving_proto_field_name=True,
        )
        assert len(json_output["flights_list"]) > 10  # why 10? just because...


@pytest.mark.asyncio
async def test_livefeed_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await livefeed_world_data(client)
        assert len(data) > 100  # why 100? just because...


@pytest.mark.asyncio
async def test_livefeed_playback_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await livefeed_playback_world_data(
            client, int(time.time() - 86400)
        )
        assert len(data) > 100


@pytest.mark.asyncio
async def test_aircraft() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await flight_list(client, reg="F-HNAV")
        df = flight_list_df(list_)
        if df is None:
            return
        assert df.shape[0] > 0
        landed = df.query('status.str.startswith("Landed")')
        if landed.shape[0] == 0:
            return
        result = await asyncio.gather(
            *[
                playback(
                    client,
                    entry["identification"]["id"],  # type: ignore
                    entry["time"]["scheduled"]["arrival"],
                )
                # the entry below is not None because of `if df is None:`
                for entry in list_["result"]["response"]["data"]  # type: ignore
                if entry["status"]["text"].startswith("Landed")
            ]
        )
        assert len(result) == landed.shape[0]


@pytest.mark.asyncio
async def test_find() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "Toulouse")
        assert list_ is not None
        assert list_["stats"]["count"]["airport"] >= 2  # includes Francazal
