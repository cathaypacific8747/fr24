from __future__ import annotations

import httpx

from .proto import encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    Geolocation,
    NearestFlightsRequest,
    NearestFlightsResponse,
)
from .types.authentication import Authentication


def nearest_flights_message_create(
    lat: float,
    lon: float,
    radius: int,
    limit: int = 1500,
) -> NearestFlightsRequest:
    """
    Create the LiveFeedRequest protobuf message

    :param lat: Centerpoint latitude (degrees)
    :param lon: Centerpoint longitude (degrees)
    :param radius: Circle radius (metres)
    :param limit: Max number of flights
    """
    return NearestFlightsRequest(
        location=Geolocation(lat=lat, lon=lon),
        radius=radius,
        limit=limit,
    )


def nearest_flights_request_create(
    message: NearestFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/NearestFlights",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def nearest_flights_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> NearestFlightsResponse:
    """Send the request and parse the protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, NearestFlightsResponse)
