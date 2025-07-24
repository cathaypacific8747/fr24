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
from fr24.proto import parse_data
from fr24.proto.headers import get_grpc_headers


async def flight_details_data() -> FlightDetailsResponse:
    headers = httpx.Headers(get_grpc_headers(auth=None))
    async with httpx.AsyncClient() as client:
        params = FlightDetailsParams(flight_id=0x3a7e02c1)
        response = await flight_details(client, params, headers)
        return parse_data(response.content, FlightDetailsResponse).unwrap()

data = await flight_details_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
aircraft_info {
  icao_address: 7901761
  reg: "B-LQD"
  type: "A359"
  icon: A330
  full_description: "Airbus A350-941"
  images_list {
    url: "https://www.jetphotos.com/photo/11697954"
    copyright: "David Li"
    thumbnail: "https://cdn.jetphotos.com/200/5/675179_1744593599_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/5/675179_1744593599.jpg"
    large: "https://cdn.jetphotos.com/640/5/675179_1744593599.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11703546"
    copyright: "Michael Eaton"
    thumbnail: "https://cdn.jetphotos.com/200/6/528687_1745054061_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/528687_1745054061.jpg"
    large: "https://cdn.jetphotos.com/640/6/528687_1745054061.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11682674"
    copyright: "Dominic Oakes"
    thumbnail: "https://cdn.jetphotos.com/200/6/649488_1743374705_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/649488_1743374705.jpg"
    large: "https://cdn.jetphotos.com/640/6/649488_1743374705.jpg"
  }
  msn_available: true
  age_available: true
  registered_owners: "Cathay Pacific"
  is_country_of_reg_available: true
}
schedule_info {
  flight_number: "CX748"
  operated_by_id: 57
  painted_as_id: 57
  origin_id: 1627
  destination_id: 1366
  scheduled_departure: 1748164800
  scheduled_arrival: 1748212200
  actual_departure: 1748165560
  arr_terminal: "1"
}
flight_progress {
  traversed_distance: 8271718
  remaining_distance: 2474032
  elapsed_time: 33428
  remaining_time: 11700
  eta: 1748210688
  great_circle_distance: 10671581
  mean_flight_time: 44471
  flight_stage: AIRBORNE
  delay_status: GREEN
  progress_pct: 74
}
flight_info {
  flightid: 981336769
  lat: 7.2621026
  lon: 96.8550873
  track: 60
  alt: 41000
  speed: 446
  timestamp_ms: 1748198985330
  callsign: "CPA748"
  ems_availability {
    qnh_availability: true
    amcp_availability: true
    oat_availability: true
    ias_availability: true
    tas_availability: true
    mach_availability: true
    agps_availability: true
    agpsdiff_availability: true
    wind_dir_availability: true
    wind_speed_availability: true
  }
  squawk_availability: true
  vspeed_availability: true
  airspace_availability: true
  server_time_ms: 1748198988037
}
flight_plan {
}
flight_trail_list {
  snapshot_id: 1748164567
  lat: -26.1300163
  lon: 28.23349
  heading: 320
}
...
flight_trail_list {
  snapshot_id: 1748198963
  lat: 7.23896599
  lon: 96.814743
  altitude: 41000
  spd: 445
  heading: 60
}
# --8<-- [end:output0]
"""
