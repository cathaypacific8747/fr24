import time

import httpx
import pytest
from fr24.core import FR24
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
async def test_ll_simple() -> None:
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
        assert len(json_output["flights_list"]) > 10


@pytest.mark.asyncio
async def test_ll_livefeed_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await livefeed_world_data(client)
        assert len(data) > 100


@pytest.mark.asyncio
async def test_ll_livefeed_playback_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await livefeed_playback_world_data(
            client, int(time.time() - 86400)
        )
        assert len(data) > 100


# core tests


@pytest.mark.asyncio
async def test_livefeed_live_world() -> None:
    async with FR24() as fr24:
        response = await fr24.livefeed.fetch()
        assert len(response.data) > 100

        datac = response.to_arrow()
        assert datac.data.num_rows == len(response.data)


@pytest.mark.asyncio
async def test_livefeed_playback_world() -> None:
    async with FR24() as fr24:
        yesterday = int(time.time() - 86400)
        response = await fr24.livefeed.fetch(yesterday)
        assert len(response.data) > 100


@pytest.mark.asyncio
async def test_livefeed_file_ops() -> None:
    """ensure context persists after serialisation to parquet"""
    async with FR24() as fr24:
        response = await fr24.livefeed.fetch()
        datac = response.to_arrow()
        datac.save()

        datac_local = fr24.livefeed.load(datac.ctx["timestamp"])
        assert datac_local.data.equals(datac.data)
        assert datac_local.data.schema.metadata == datac.data.schema.metadata
