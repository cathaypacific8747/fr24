# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import live_flights_status
from fr24.proto.v1_pb2 import LiveFlightsStatusRequest, LiveFlightsStatusResponse


async def live_flights_status_data() -> LiveFlightsStatusResponse:
    async with httpx.AsyncClient() as client:
        message = LiveFlightsStatusRequest(flight_ids_list=[0x35fbc363, 0x35fbf180])
        result = await live_flights_status(client, message)
        return result.unwrap()


data = await live_flights_status_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
flights_map {
  flight_id: 905703808
  data {
    lat: 21.7237415
    lon: 114.917908
    status: LIVE
  }
}
flights_map {
  flight_id: 905692003
  data {
    lat: 21.9285736
    lon: 113.912445
    status: LIVE
  }
}
# --8<-- [end:output0]
"""
