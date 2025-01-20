import time

import httpx
import pytest
from google.protobuf.json_format import MessageToDict

from fr24 import FR24
from fr24.grpc import (
    BoundingBox,
    LiveFeedParams,
    live_feed,
    live_feed_parse,
)


@pytest.mark.anyio
async def test_ll_live_feed_simple(client: httpx.AsyncClient) -> None:
    params = LiveFeedParams(
        bounding_box=BoundingBox(north=50, west=-7, south=40, east=10)
    )
    response = await live_feed(client, params)
    data = live_feed_parse(response)

    json_output = MessageToDict(
        data,
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
    result = await fr24.live_feed.fetch()
    len_proto = len(result.to_proto().flights_list)
    assert len_proto > 100

    df = result.to_polars()
    assert df.height == len_proto


@pytest.mark.anyio
async def test_live_feed_playback_world(fr24: FR24) -> None:
    yesterday = int(time.time() - 86400)
    result = await fr24.live_feed_playback.fetch(timestamp=yesterday)
    assert result.to_polars().height > 100


@pytest.mark.anyio
async def test_live_feed_file_ops(fr24: FR24) -> None:
    """ensure context persists after serialisation to parquet"""
    result = await fr24.live_feed.fetch()
    result.save()

    result_local = fr24.live_feed.load(result.timestamp)
    assert result_local.to_polars() == result.to_polars()
    # assert datac_local.data.schema.metadata == datac.data.schema.metadata
