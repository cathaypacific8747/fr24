# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    historic_trail_request_create,
    historic_trail,
)
from fr24.proto.v1_pb2 import HistoricTrailRequest, HistoricTrailResponse


async def historic_trail_data() -> HistoricTrailResponse:
    async with httpx.AsyncClient() as client:
        message = HistoricTrailRequest(flight_id=0x395c43cf)
        request = historic_trail_request_create(message)
        result = await historic_trail(client, request)
        return result.unwrap()

data = await historic_trail_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
504 GATEWAY TIMEOUT
# --8<-- [end:output0]
"""
