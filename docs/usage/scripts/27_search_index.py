# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    search_index_request_create,
    search_index,
)
from fr24.proto.v1_pb2 import FetchSearchIndexRequest, FetchSearchIndexResponse


async def search_index_data() -> FetchSearchIndexResponse:
    async with httpx.AsyncClient() as client:
        message = FetchSearchIndexRequest()
        request = search_index_request_create(message)
        result = await search_index(client, request)
        return result.unwrap()


data = await search_index_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]

# --8<-- [end:output0]
"""
