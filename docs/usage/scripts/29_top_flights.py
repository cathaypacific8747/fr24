# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.top_flights import (
    top_flights_request_create,
    top_flights_post,
)
from fr24.proto.v1_pb2 import TopFlightsRequest, TopFlightsResponse


async def top_flights_data() -> TopFlightsResponse:
    async with httpx.AsyncClient() as client:
        message = TopFlightsRequest(limit=10)
        request = top_flights_request_create(message)
        return await top_flights_post(client, request)


data = await top_flights_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]

# --8<-- [end:output0]
"""
