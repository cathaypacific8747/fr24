import asyncio
import time

import httpx
import pytest
from google.protobuf.json_format import MessageToDict

from fr24 import FR24, Cache
from fr24.grpc import (
    BBOX_FRANCE_UIR,
    BBOXES_WORLD_STATIC,
    BoundingBox,
    LiveFeedParams,
    LiveFeedPlaybackParams,
    live_feed,
    live_feed_parse,
    live_feed_playback,
    live_feed_playback_parse,
)
from fr24.proto.v1_pb2 import Flight


@pytest.mark.anyio
async def test_ll_live_feed_simple(client: httpx.AsyncClient) -> None:
    params = LiveFeedParams(bounding_box=BBOX_FRANCE_UIR)
    response = await live_feed(client, params)
    result = live_feed_parse(response)

    json_output = MessageToDict(
        result.unwrap(),
        use_integers_for_enums=False,
        preserving_proto_field_name=True,
    )
    assert len(json_output["flights_list"]) > 10


@pytest.mark.anyio
async def test_ll_live_feed_world(client: httpx.AsyncClient) -> None:
    async def get_data(bbox: BoundingBox) -> list[Flight]:
        params = LiveFeedParams(bounding_box=bbox)
        response = await live_feed(client, params)
        result = live_feed_parse(response)
        return list(result.unwrap().flights_list)

    tasks = [get_data(bbox) for bbox in BBOXES_WORLD_STATIC]
    flightss = await asyncio.gather(*tasks)
    assert all(len(f) > 0 for f in flightss)
    assert len([f for flights in flightss for f in flights]) > 100


@pytest.mark.anyio
async def test_ll_live_feed_playback_world(client: httpx.AsyncClient) -> None:
    timestamp = int(time.time() - 86400)

    async def get_data(bbox: BoundingBox) -> list[Flight]:
        params = LiveFeedPlaybackParams(bounding_box=bbox, timestamp=timestamp)
        response = await live_feed_playback(client, params)
        result = live_feed_playback_parse(response)
        return list(result.unwrap().live_feed_response.flights_list)

    tasks = [get_data(bbox) for bbox in BBOXES_WORLD_STATIC]
    flightss = await asyncio.gather(*tasks)
    assert all(len(f) > 0 for f in flightss)
    assert len([f for flights in flightss for f in flights]) > 100


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
async def test_live_feed_file_ops(fr24: FR24, cache: Cache) -> None:
    """ensure context persists after serialisation to parquet"""
    result = await fr24.live_feed.fetch()
    result.write_table(cache)

    df_local = cache.live_feed.scan_table(result.timestamp).collect()
    assert df_local.equals(result.to_polars())
    # NOTE: metadata serialisation is not implemented
