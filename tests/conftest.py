import tempfile
from pathlib import Path
from typing import AsyncGenerator

import httpx
import pytest

from fr24.core import FR24


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture(scope="session", autouse=True)
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    async with httpx.AsyncClient(http1=False, http2=True) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def fr24() -> AsyncGenerator[FR24, None]:
    async with FR24(base_dir=Path(tempfile.gettempdir()) / "fr24") as fr24:
        yield fr24
