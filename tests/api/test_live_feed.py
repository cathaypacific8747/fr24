import time

import httpx
import pytest
from google.protobuf.json_format import MessageToDict

from fr24.core import FR24
from fr24.grpc import (
    live_feed_message_create,
    live_feed_playback_world_data,
    live_feed_post,
    live_feed_request_create,
    live_feed_world_data,
)


@pytest.mark.anyio
async def test_ll_live_feed_simple(client: httpx.AsyncClient) -> None:
    message = live_feed_message_create(north=50, west=-7, south=40, east=10)
    request = live_feed_request_create(message)
    result = await live_feed_post(client, request)

    json_output = MessageToDict(
        result,
        use_integers_for_enums=False,
        preserving_proto_field_name=True,
    )
    assert len(json_output["flights_list"]) > 10


@pytest.mark.anyio
async def test_ll_live_feed_world(client: httpx.AsyncClient) -> None:
    data = await live_feed_world_data(client)
    assert len(data) > 100


@pytest.mark.anyio
async def test_ll_live_feed_playback_world(client: httpx.AsyncClient) -> None:
    data = await live_feed_playback_world_data(client, int(time.time() - 86400))
    assert len(data) > 100


# core tests


@pytest.mark.anyio
async def test_live_feed_live_world(fr24: FR24) -> None:
    response = await fr24.live_feed.fetch()
    assert len(response.data) > 100

    datac = response.to_arrow()
    assert datac.data.num_rows == len(response.data)


@pytest.mark.anyio
async def test_live_feed_playback_world(fr24: FR24) -> None:
    yesterday = int(time.time() - 86400)
    response = await fr24.live_feed.fetch(yesterday)
    assert len(response.data) > 100


@pytest.mark.anyio
async def test_live_feed_file_ops(fr24: FR24) -> None:
    """ensure context persists after serialisation to parquet"""
    response = await fr24.live_feed.fetch()
    datac = response.to_arrow()
    datac.save()

    datac_local = fr24.live_feed.load(datac.ctx["timestamp"])
    assert datac_local.data.equals(datac.data)
    assert datac_local.data.schema.metadata == datac.data.schema.metadata
