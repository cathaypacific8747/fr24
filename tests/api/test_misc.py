import httpx
import pytest
from fr24.find import find


@pytest.mark.asyncio
async def test_find() -> None:
    async with httpx.AsyncClient() as client:
        list_ = await find(client, "Toulouse")
        assert list_ is not None
        assert list_["stats"]["count"]["airport"] >= 2  # includes Francazal
