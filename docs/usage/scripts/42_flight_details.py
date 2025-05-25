# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import (
    FlightDetailsParams,
    flight_details,
)
from fr24.proto.v1_pb2 import FlightDetailsResponse


async def flight_details_data() -> FlightDetailsResponse:
    async with httpx.AsyncClient() as client:
        params = FlightDetailsParams(flight_id=0x3a71abce)
        result = await flight_details(client, params)
        return result.unwrap()

data = await flight_details_data()
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
  flight_number: "CX100"
  operated_by_id: 57
  painted_as_id: 57
  origin_id: 3370
  destination_id: 1366
  scheduled_departure: 1747886700
  scheduled_arrival: 1747920600
  actual_departure: 1747887360
  arr_terminal: "1"
}
flight_progress {
  traversed_distance: 1445203
  remaining_distance: 5940859
  elapsed_time: 7239
  remaining_time: 25529
  eta: 1747920128
  great_circle_distance: 7371723
  mean_flight_time: 31849
  flight_stage: AIRBORNE
  delay_status: GREEN
  progress_pct: 22
}
flight_info {
  flightid: 980528078
  lat: -22.474535
  lon: 144.153641
  track: 343
  alt: 38000
  speed: 427
  timestamp_ms: 1747894597000
  callsign: "CPA100"
  ems_availability {
    qnh_availability: true
    amcp_availability: true
    oat_availability: true
    ias_availability: true
    tas_availability: true
    mach_availability: true
    agps_availability: true
    agpsdiff_availability: true
  }
  squawk_availability: true
  vspeed_availability: true
  airspace_availability: true
  server_time_ms: 1747894599299
}
flight_plan {
}
flight_trail_list {
  snapshot_id: 1747886571
  lat: -33.9357681
  lon: 151.167923
  heading: 239
}
flight_trail_list {
  snapshot_id: 1747886659
  lat: -33.9356575
  lon: 151.168137
...
flight_trail_list {
  snapshot_id: 1747894543
  lat: -22.5770912
  lon: 144.187012
  altitude: 38000
  spd: 426
  heading: 343
}
# --8<-- [end:output0]
"""
