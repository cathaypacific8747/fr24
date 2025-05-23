# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    playback_flight_request_create,
    playback_flight,
)
from fr24.proto.v1_pb2 import PlaybackFlightRequest, PlaybackFlightResponse


async def playback_flight_data() -> PlaybackFlightResponse:
    async with httpx.AsyncClient() as client:
        message = PlaybackFlightRequest(flight_id=0x3a6d881a, timestamp=1747794900)
        request = playback_flight_request_create(message)
        result = await playback_flight(client, request)
        return result.unwrap()

data = await playback_flight_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
aircraft_info {
  icao_address: 7867035
  type: "A359"
  icon: A330
  full_description: "Airbus A350-941"
  images_list {
    url: "https://www.jetphotos.com/photo/11633658"
    copyright: "lix1aolu"
    thumbnail: "https://cdn.jetphotos.com/200/6/850117_1739185739_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/850117_1739185739.jpg"
    large: "https://cdn.jetphotos.com/640/6/850117_1739185739.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11634217"
    copyright: "Waibibabu"
    thumbnail: "https://cdn.jetphotos.com/200/6/591483_1739217827_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/591483_1739217827.jpg"
    large: "https://cdn.jetphotos.com/640/6/591483_1739217827.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11620028"
    copyright: "ZBAA cao"
    thumbnail: "https://cdn.jetphotos.com/200/6/723478_1737987561_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/723478_1737987561.jpg"
    large: "https://cdn.jetphotos.com/640/6/723478_1737987561.jpg"
  }
  msn_available: true
  age_available: true
  registered_owners: "Cathay Pacific"
  is_country_of_reg_available: true
}
schedule_info {
  flight_number: "CX150"
  operated_by_id: 57
  painted_as_id: 57
  origin_id: 431
  destination_id: 1366
  scheduled_departure: 1747794900
  scheduled_arrival: 1747827000
  actual_departure: 1747796246
  actual_arrival: 1747826241
  arr_terminal: "1"
  baggage_belt: "2"
}
flight_info {
  flightid: 980256794
  lat: -27.4022541
  lon: 153.113098
  track: 30
  speed: 1
  timestamp_ms: 1747794874975
  on_ground: true
  callsign: "CPA150"
  ems_availability {
  }
  squawk_availability: true
  vspeed_availability: true
  airspace_availability: true
  server_time_ms: 1747895055592
}
flight_trail_list {
  snapshot_id: 1747794677
  lat: -27.4009781
  lon: 153.112823
  heading: 306
}
flight_trail_list {
  snapshot_id: 1747794731
  lat: -27.4011135
  lon: 153.113037
  spd: 2
  heading: 312
}
...
flight_trail_list {
  snapshot_id: 1747827307
  lat: 22.3126259
  lon: 113.925751
  heading: 53
}
"""
