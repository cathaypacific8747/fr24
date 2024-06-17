import time

import pytest
from fr24.core import FR24


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
