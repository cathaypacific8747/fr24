from __future__ import annotations

import httpx

from .proto import encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    LiveFlightsStatusRequest,
    LiveFlightsStatusResponse,
)
from .types.authentication import Authentication


def live_flights_status_request_create(
    message: LiveFlightsStatusRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFlightsStatus",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def live_flights_status_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveFlightsStatusResponse:
    """Send the request and parse the protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, LiveFlightsStatusResponse)
