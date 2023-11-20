import asyncio

import httpx
import pytest
from fr24.history import flight_list, flight_list_df, playback
from fr24.livefeed import create_request, post_request, world_data
from google.protobuf.json_format import MessageToDict

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_simple() -> None:
    request = create_request()
    async with httpx.AsyncClient() as client:
        result = await post_request(client, request)
        assert result is not None

        json_output = MessageToDict(
            result,
            including_default_value_fields=True,
            use_integers_for_enums=False,
            preserving_proto_field_name=True,
        )
        assert len(json_output["flights_list"]) > 10  # why 10? just because...


@pytest.mark.asyncio
async def test_world() -> None:
    async with httpx.AsyncClient() as client:
        df = await world_data(client)
        assert df.shape[0] > 100  # why 100? same, because...


@pytest.mark.asyncio
async def test_aircraft() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await flight_list(client, reg="F-HNAV")
        df = flight_list_df(list_)
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
                for entry in list_["result"]["response"]["data"]
                if entry["status"]["text"].startswith("Landed")
            ]
        )
        assert len(result) == landed.shape[0]
