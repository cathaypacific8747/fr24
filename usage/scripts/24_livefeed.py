# ruff: noqa
# fmt: off
# %%
# --8<-- [start:script0]
import httpx
from fr24.livefeed import (
    livefeed_message_create,
    livefeed_post,
    livefeed_request_create,
    livefeed_response_parse,
)
from fr24.proto.request_pb2 import LiveFeedResponse


async def france_data() -> LiveFeedResponse:
    async with httpx.AsyncClient() as client:
        message = livefeed_message_create(north=50, west=-7, south=40, east=10)
        request = livefeed_request_create(message)
        data = await livefeed_post(client, request)
        return livefeed_response_parse(data)


data = await france_data()
data
# --8<-- [end:script0]
#%%
"""
# --8<-- [start:output0]
flights_list {
  flightid: 882295486
  latitude: 40.4882507
  longitude: -6.38517904
  track: 33
  altitude: 36000
  ground_speed: 454
  icon: 7
  timestamp: 1711960343
  callsign: "BTI4PX"
  extra_info {
    flight: "BT766"
    reg: "YL-ABL"
    route {
      from_: "LPA"
      to: "RIX"
    }
    type: "BCS3"
  }
}
flights_list {
  flightid: 882307182
  latitude: 40.1034851
  longitude: -4.40472412
  track: 162
...
      to: "HRG"
    }
    type: "B738"
  }
}
# --8<-- [end:output0]
"""
# %% [markdown]
# # explore in JSON format
# take a look at src/fr24/livefeed.py to find more examples about how to use it

# %%
# --8<-- [start:script1]
from google.protobuf.json_format import MessageToDict

MessageToDict(data)["flightsList"]
# --8<-- [end:script1]
#%%
"""
# --8<-- [start:output1]
[{'flightid': 882295486,
  'latitude': 40.48825,
  'longitude': -6.385179,
  'track': 33,
  'altitude': 36000,
  'groundSpeed': 454,
  'icon': 7,
  'timestamp': 1711960343,
  'callsign': 'BTI4PX',
  'extraInfo': {'flight': 'BT766',
   'reg': 'YL-ABL',
   'route': {'from': 'LPA', 'to': 'RIX'},
   'type': 'BCS3'}},
 {'flightid': 882307182,
  'latitude': 40.103485,
  'longitude': -4.404724,
  'track': 162,
  'altitude': 32950,
  'groundSpeed': 513,
  'icon': 10,
  'timestamp': 1711960344,
  'callsign': 'EVE1123',
  'extraInfo': {'flight': 'E91123',
   'reg': 'EC-LZD',
   'route': {'from': 'VLL', 'to': 'AGP'},
...
  'callsign': 'CXI1015',
  'extraInfo': {'flight': 'XR1015',
   'reg': '9H-CXE',
   'route': {'from': 'CGN', 'to': 'HRG'},
   'type': 'B738'}}]
# --8<-- [end:output1]
"""
# %%
