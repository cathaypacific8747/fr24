from __future__ import annotations

from typing import AsyncIterator

import httpx

from .proto import encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    FollowFlightRequest,
    FollowFlightResponse,
)
from .types.authentication import Authentication


def follow_flight_request_create(
    message: FollowFlightRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/FollowFlight",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def follow_flight_stream(
    client: httpx.AsyncClient, request: httpx.Request
) -> AsyncIterator[FollowFlightResponse]:
    """Send the request and parse each streaming response protobuf message."""
    response = await client.send(request, stream=True)
    try:
        async for chunk in response.aiter_bytes():
            yield parse_data(chunk, FollowFlightResponse)
    finally:
        await response.aclose()
