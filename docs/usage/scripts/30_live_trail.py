# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    live_trail_request_create,
    live_trail_post,
)
from fr24.proto.v1_pb2 import LiveTrailRequest, LiveTrailResponse


async def live_trail_data() -> LiveTrailResponse:
    """raises empty `DATA` frame error if flight_id is not live"""
    async with httpx.AsyncClient() as client:
        message = LiveTrailRequest(flight_id=0x395c43cf)
        request = live_trail_request_create(message)
        return await live_trail_post(client, request)


data = await live_trail_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
radar_records_list {
  timestamp: 1720064455
  lat: 30.2406578
  lon: 120.420403
  spd: 15
  heading: 61
  callsign: "CPA959"
}
radar_records_list {
  timestamp: 1720064462
  lat: 30.2408924
  lon: 120.420937
  heading: 61
  callsign: "CPA959"
}
radar_records_list {
  timestamp: 1720064480
  lat: 30.2415791
  lon: 120.422478
  spd: 18
  heading: 61
  callsign: "CPA959"
}
radar_records_list {
  timestamp: 1720064488
...
  heading: 269
  vspd: -960
  squawk: 13874
  callsign: "CPA959"
}
...
# --8<-- [end:output0]
"""
