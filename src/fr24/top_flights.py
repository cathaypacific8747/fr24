from __future__ import annotations

import httpx

from .proto import encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    TopFlightsRequest,
    TopFlightsResponse,
)
from .types.authentication import Authentication


def top_flights_request_create(
    message: TopFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/TopFlights",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def top_flights_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> TopFlightsResponse:
    """Send the request and parse the protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, TopFlightsResponse)
