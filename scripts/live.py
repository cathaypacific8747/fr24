# %%
# ruff: noqa: F704, F811, E402
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


data = await france_data()  # type: ignore
# %% [markdown]
# # explore in JSON format
# take a look at src/fr24/livefeed.py to find more examples about how to use it

# %%
from google.protobuf.json_format import MessageToDict

MessageToDict(data)["flightsList"]

# %%
