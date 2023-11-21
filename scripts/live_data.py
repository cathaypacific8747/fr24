# ruff: noqa: F704, F811, E402
# %%
import httpx
from fr24.livefeed import create_request, post_request
from fr24.proto.request_pb2 import LiveFeedResponse


async def france_data() -> LiveFeedResponse:
    async with httpx.AsyncClient() as client:
        request = create_request(north=50, west=-7, south=40, east=10)
        live_data = await post_request(client, request)
        return live_data


data = await france_data()  # type: ignore
data

# %%
from google.protobuf.json_format import MessageToDict

# explore in JSON format
MessageToDict(data)

# Look at the code in livefeed.py to find more examples about how to use it
