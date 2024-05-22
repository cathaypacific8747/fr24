import time

import pytest
from fr24.core import FR24


@pytest.mark.asyncio
async def test_livefeed_live_world() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed()
        response = await lf.api._fetch()
        assert len(response) > 100
        lf.data._add_api_response(response)
        with pytest.raises(NotImplementedError):  # concatenation
            lf.data._add_api_response(response)
        assert lf.data.table is not None
        assert lf.data.table.num_rows == len(response)


@pytest.mark.asyncio
async def test_livefeed_playback_world() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed(int(time.time() - 86400))
        response = await lf.api._fetch()
        assert len(response) > 100
        lf.data._add_api_response(response)
        assert lf.data.table is not None
        assert lf.data.table.num_rows == len(response)


@pytest.mark.asyncio
async def test_livefeed_playback_world_with_duration() -> None:
    async with FR24() as fr24:
        lf = fr24.livefeed(int(time.time() - 86400), duration=30)
        response = await lf.api._fetch()
        assert len(response) > 100
        lf.data._add_api_response(response)
        assert lf.data.table is not None
        assert lf.data.table.num_rows == len(response)


@pytest.mark.asyncio
async def test_livefeed_file_ops() -> None:
    """ensure context persists after serialisation to parquet"""
    async with FR24() as fr24:
        lf = fr24.livefeed()
        lf.data._add_api_response(await lf.api._fetch())
        lf.data._save_parquet()

        lf2 = fr24.livefeed(lf.ctx["timestamp"])
        lf2.data._from_file()
        assert lf2.data.table is not None
        assert lf2.data.table.equals(lf.data.table)
        assert lf2.data.schema.metadata == lf.data.schema.metadata


@pytest.mark.asyncio
async def test_livefeed_live_uninitialised() -> None:
    """
    timestamp is not set until .api.fetch() is called: calling .fp should raise
    """
    async with FR24() as fr24:
        lf = fr24.livefeed()
        with pytest.raises(ValueError):
            _ = lf.data.fp
