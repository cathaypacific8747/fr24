import httpx
import pytest
from fr24.livefeed import create_request, post_request, world_data
from google.protobuf.json_format import MessageToDict

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_simple() -> None:
    request = create_request()
    async with httpx.AsyncClient() as client:
        result = await post_request(client, request)
        assert result is not None

        json_output = MessageToDict(
            result,
            including_default_value_fields=True,
            use_integers_for_enums=False,
            preserving_proto_field_name=True,
        )
        assert len(json_output["flights_list"]) > 10  # why 10? just because...


@pytest.mark.asyncio
async def test_world() -> None:
    async with httpx.AsyncClient() as client:
        df = await world_data(client)
        assert df.shape[0] > 100  # why 100? same, because...
