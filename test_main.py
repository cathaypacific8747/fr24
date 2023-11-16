import pytest
from main import download_simple, download_full

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_simple():
    await download_simple()

@pytest.mark.asyncio
async def test_globe():
    await download_full()