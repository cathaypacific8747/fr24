import time

import httpx
import pytest
from fr24.core import FR24
from fr24.live_feed import (
    live_feed_message_create,
    live_feed_playback_world_data,
    live_feed_post,
    live_feed_request_create,
    live_feed_world_data,
)
from google.protobuf.json_format import MessageToDict


@pytest.mark.asyncio
async def test_ll_live_feed_simple() -> None:
    message = live_feed_message_create(north=50, west=-7, south=40, east=10)
    request = live_feed_request_create(message)
    async with httpx.AsyncClient() as client:
        result = await live_feed_post(client, request)

        json_output = MessageToDict(
            result,
            use_integers_for_enums=False,
            preserving_proto_field_name=True,
        )
        assert len(json_output["flights_list"]) > 10


@pytest.mark.asyncio
async def test_ll_live_feed_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await live_feed_world_data(client)
        assert len(data) > 100


@pytest.mark.asyncio
async def test_ll_live_feed_playback_world() -> None:
    async with httpx.AsyncClient() as client:
        data = await live_feed_playback_world_data(
            client, int(time.time() - 86400)
        )
        assert len(data) > 100


# core tests


@pytest.mark.asyncio
async def test_live_feed_live_world() -> None:
    async with FR24() as fr24:
        response = await fr24.live_feed.fetch()
        assert len(response.data) > 100

        datac = response.to_arrow()
        assert datac.data.num_rows == len(response.data)


@pytest.mark.asyncio
async def test_live_feed_playback_world() -> None:
    async with FR24() as fr24:
        yesterday = int(time.time() - 86400)
        response = await fr24.live_feed.fetch(yesterday)
        assert len(response.data) > 100


@pytest.mark.asyncio
async def test_live_feed_file_ops() -> None:
    """ensure context persists after serialisation to parquet"""
    async with FR24() as fr24:
        response = await fr24.live_feed.fetch()
        datac = response.to_arrow()
        datac.save()

        datac_local = fr24.live_feed.load(datac.ctx["timestamp"])
        assert datac_local.data.equals(datac.data)
        assert datac_local.data.schema.metadata == datac.data.schema.metadata
