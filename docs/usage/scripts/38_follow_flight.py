# ruff: noqa
# fmt: off
# mypy: disable-error-code="top-level-await, no-redef"
# %%
# --8<-- [start:script0]
import httpx
from fr24.grpc import follow_flight_stream
from fr24.proto.v1_pb2 import FollowFlightRequest

async def follow_flight_data() -> None:
    # NOTE: fr24 often sends state vector packets every 1-60 seconds,
    # but httpx by default closes the stream after 5 seconds. We
    # increase the timeout to 120 seconds to avoid premature closure.
    timeout = httpx.Timeout(5, read=120)
    async with httpx.AsyncClient(timeout=timeout) as client:
        message = FollowFlightRequest(flight_id=0x395c43cf)
        i = 0
        async for response in follow_flight_stream(client, message):
            print(f"##### {i} #####")
            print(response)
            i += 1
            if i > 3:
                break

await follow_flight_data()
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
##### 0 #####
aircraft_info {
  icao_address: 5031041
  type: "B744"
  icon: B747
  full_description: "Boeing 747-48EF"
  service: CARGO
  images_list {
    url: "https://www.jetphotos.com/photo/11372499"
    copyright: "R Skywalker"
    thumbnail: "https://cdn.jetphotos.com/200/5/609890_1717848712_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/5/609890_1717848712.jpg"
    large: "https://cdn.jetphotos.com/640/5/609890_1717848712.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11358154"
    copyright: "Tim-Patrick Müller"
    thumbnail: "https://cdn.jetphotos.com/200/5/1615840_1716633484_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/5/1615840_1716633484.jpg"
    large: "https://cdn.jetphotos.com/640/5/1615840_1716633484.jpg"
  }
  images_list {
    url: "https://www.jetphotos.com/photo/11337719"
    copyright: "Siegi N."
    thumbnail: "https://cdn.jetphotos.com/200/6/417379_1714816605_tb.jpg"
    medium: "https://cdn.jetphotos.com/400/6/417379_1714816605.jpg"
    large: "https://cdn.jetphotos.com/640/6/417379_1714816605.jpg"
  }
  msn_available: true
  age_available: true
  registered_owners: "Network Aviation"
}
flight_plan {
}
schedule_info {
  flight_number: "CC4400"
  operated_by_id: 437
  origin_id: 1366
  actual_departure: 1720074023
}
flight_progress {
  elapsed_time: 1611
}
flight_info {
  flightid: 905705829
  lat: 21.2512665
  lon: 112.568764
  track: 278
  alt: 31000
  speed: 512
  timestamp: 1720075629
  callsign: "ABD4400"
  ems_availability {
    amcp_availability: true
    oat_availability: true
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
}
flight_trail_list {
  snapshot_id: 1720073072
  lat: 22.3014889
  lon: 113.923706
  heading: 340
}
flight_trail_list {
  snapshot_id: 1720073114
  lat: 22.3012848
  lon: 113.92379
  spd: 3
  heading: 340
}

...
  altitude: 31000
  spd: 512
  heading: 278
}

##### 1 #####
schedule_info {
  flight_number: "CC4400"
  operated_by_id: 437
  origin_id: 1366
  actual_departure: 1720074023
}
flight_progress {
  elapsed_time: 1615
}
flight_info {
  flightid: 905705829
  lat: 21.2530975
  lon: 112.555733
  track: 278
  alt: 31000
  speed: 512
  timestamp: 1720075634
  callsign: "ABD4400"
  ems_availability {
    amcp_availability: true
    oat_availability: true
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
}

##### 2 #####
schedule_info {
  flight_number: "CC4400"
  operated_by_id: 437
  origin_id: 1366
  actual_departure: 1720074023
}
flight_progress {
  elapsed_time: 1619
}
flight_info {
  flightid: 905705829
  lat: 21.2530975
  lon: 112.555733
  track: 278
  alt: 31000
  speed: 512
  timestamp: 1720075634
  callsign: "ABD4400"
  ems_availability {
    amcp_availability: true
    oat_availability: true
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
}

##### 3 #####
schedule_info {
  flight_number: "CC4400"
  operated_by_id: 437
  origin_id: 1366
  actual_departure: 1720074023
}
flight_progress {
  elapsed_time: 1623
}
flight_info {
  flightid: 905705829
  lat: 21.2557068
  lon: 112.537407
  track: 278
  alt: 31000
  speed: 512
  timestamp: 1720075641
  callsign: "ABD4400"
...
# --8<-- [end:output0]
"""
