# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    top_flights_request_create,
    top_flights_post,
)
from fr24.proto.v1_pb2 import TopFlightsRequest, TopFlightsResponse


async def top_flights_data() -> TopFlightsResponse:
    async with httpx.AsyncClient() as client:
        message = TopFlightsRequest(limit=10)
        request = top_flights_request_create(message)
        result = await top_flights_post(client, request)
        return result.unwrap()


data = await top_flights_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
scoreboard_list {
  flight_id: 911336284
  live_clicks: 1648
  total_clicks: 6664
  callsign: "LEE92"
  from_iata: "QKG"
  from_city: "Leeming"
  type: "HUNT"
  full_description: "Hawker Hunter T2"
}
scoreboard_list {
  flight_id: 911326556
  live_clicks: 1144
  total_clicks: 8848
  callsign: "SARAB"
  type: "HAWK"
  full_description: "British Aerospace Hawk Mk167"
}
scoreboard_list {
  flight_id: 911338539
  live_clicks: 904
  total_clicks: 1764
  flight_number: "TN80001"
  callsign: "TN080001"
  from_iata: "QCY"
...
  to_iata: "RMQ"
  to_city: "Taichung"
  type: "B738"
  full_description: "Boeing 737-8AL"
}
# --8<-- [end:output0]
"""
