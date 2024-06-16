from __future__ import annotations

import asyncio
import secrets
import struct
from typing import Any

import httpx
from loguru import logger

from .bbox import lng_bounds
from .common import DEFAULT_HEADERS_GRPC
from .proto.request_pb2 import (
    LiveFeedPlaybackRequest,
    LiveFeedPlaybackResponse,
    LiveFeedRequest,
    LiveFeedResponse,
)
from .types.cache import LiveFeedRecord
from .types.fr24 import Authentication

# N, S, W, E
world_zones = [
    (90, -90, lng_bounds[i], lng_bounds[i + 1])
    for i in range(len(lng_bounds) - 1)
]


def livefeed_message_create(
    north: float = 50,
    south: float = 40,
    west: float = 0,
    east: float = 10,
    stats: bool = False,
    limit: int = 1500,
    maxage: int = 14400,
    fields: list[str] = [
        "flight",
        "reg",
        "route",
        "type",
    ],
    **kwargs: Any,
) -> LiveFeedRequest:
    """
    Create the LiveFeedRequest protobuf message

    :param north: North latitude
    :param south: South latitude
    :param west: West longitude
    :param east: East longitude
    :param stats: Include stats of the given area
    :param limit: Max number of flights
    :param maxage: Max age since last update, seconds
    :param fields: fields to include - for unauthenticated users, max 4 fields.
        When authenticated, `squawk`, `vspeed`, `airspace`, `logo_id` and `age`
        can be included
    """
    return LiveFeedRequest(
        bounds=LiveFeedRequest.Bounds(
            north=north, south=south, west=west, east=east
        ),
        settings=LiveFeedRequest.Settings(
            sources_list=range(10),  # type: ignore
            services_list=range(12),  # type: ignore
            traffic_type=LiveFeedRequest.Settings.ALL,
            only_restricted=False,
        ),
        field_mask=LiveFeedRequest.FieldMask(field_name=fields),
        highlight_mode=False,
        stats=stats,
        limit=limit,
        maxage=maxage,
        restriction_mode=LiveFeedRequest.NOT_VISIBLE,
        **kwargs,
    )


def livefeed_playback_message_create(
    message: LiveFeedRequest,
    timestamp: int,
    prefetch: int,
    hfreq: int,
) -> LiveFeedPlaybackRequest:
    """
    Create the live feed playback request protobuf message.

    :param timestamp: Start timestamp
    :param prefetch: End timestamp: should be start timestamp + 7 seconds
    :param hfreq: High frequency mode
    """
    return LiveFeedPlaybackRequest(
        live_feed_request=message,
        timestamp=timestamp,
        prefetch=prefetch,
        hfreq=hfreq,
    )


def livefeed_request_create(
    message: LiveFeedRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    request_s = message.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s

    headers = DEFAULT_HEADERS_GRPC.copy()
    headers["fr24-device-id"] = f"web-{secrets.token_urlsafe(32)}"
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"

    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed",
        headers=headers,
        content=post_data,
    )


def livefeed_playback_request_create(
    message: LiveFeedPlaybackRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Constructs the POST request with encoded gRPC body."""
    request_s = message.SerializeToString()
    post_data = b"\x00" + struct.pack("!I", len(request_s)) + request_s

    headers = DEFAULT_HEADERS_GRPC.copy()
    headers["fr24-device-id"] = f"web-{secrets.token_urlsafe(32)}"
    if auth is not None and auth["userData"]["accessToken"] is not None:
        headers["authorization"] = f"Bearer {auth['userData']['accessToken']}"

    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/Playback",
        headers=headers,
        content=post_data,
    )


async def livefeed_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> bytes:
    """Send the request and extract the raw protobuf message."""
    response = await client.send(request)
    data = response.content
    assert len(data) and data[0] == 0
    data_len = int.from_bytes(data[1:5], byteorder="big")
    return data[5 : 5 + data_len]


def livefeed_response_parse(data: bytes) -> LiveFeedResponse:
    """:param data: raw protobuf message"""
    lfr = LiveFeedResponse()
    lfr.ParseFromString(data)
    return lfr


def livefeed_playback_response_parse(data: bytes) -> LiveFeedResponse:
    """:param data: raw protobuf message"""
    lfr = LiveFeedPlaybackResponse()
    lfr.ParseFromString(data)
    return lfr.live_feed_response


def livefeed_flightdata_dict(
    lfr: LiveFeedResponse.FlightData,
) -> LiveFeedRecord:
    """Convert the protobuf message to a dictionary."""
    return {
        "timestamp": lfr.timestamp,
        "flightid": lfr.flightid,
        "latitude": lfr.latitude,
        "longitude": lfr.longitude,
        "heading": lfr.heading,
        "altitude": lfr.altitude,
        "ground_speed": lfr.ground_speed,
        "vertical_speed": lfr.extra_info.vspeed,
        "on_ground": lfr.on_ground,
        "callsign": lfr.callsign,
        "source": lfr.source,
        "registration": lfr.extra_info.reg,
        "origin": lfr.extra_info.route.from_,
        "destination": lfr.extra_info.route.to,
        "typecode": lfr.extra_info.type,
        "eta": lfr.extra_info.schedule.eta,
    }


# TODO: add parameter for custom bounds, e.g. from .bounds.lng_bounds_per_30_min
async def livefeed_world_data(
    client: httpx.AsyncClient, auth: None | Authentication = None
) -> list[LiveFeedRecord]:
    """Retrieve live feed data for the entire world, in chunks."""
    results = await asyncio.gather(
        *[
            livefeed_post(
                client,
                livefeed_request_create(
                    livefeed_message_create(*bounds), auth=auth
                ),
            )
            for bounds in world_zones
        ]
    )
    return [
        livefeed_flightdata_dict(lfr)
        for r in results
        for lfr in livefeed_response_parse(r).flights_list
    ]


async def livefeed_playback_world_data(
    client: httpx.AsyncClient,
    timestamp: int,
    duration: int = 7,
    hfreq: int = 0,
    auth: None | Authentication = None,
) -> list[LiveFeedRecord]:
    """
    Retrieve live feed playback data for the entire world, in chunks.

    :raises Exception: if more than half of the requests fail
    """
    results = await asyncio.gather(
        *[
            livefeed_post(
                client,
                livefeed_playback_request_create(
                    livefeed_playback_message_create(
                        livefeed_message_create(*bounds),
                        timestamp,
                        timestamp + duration,
                        hfreq,
                    ),
                    auth=auth,
                ),
            )
            for bounds in world_zones
        ],
        return_exceptions=True,
    )
    if len(err := [r for r in results if not isinstance(r, bytes)]) > 0:
        logger.warning(f"{len(err)} errors: {err}!")
        if len(err) > len(results) / 2:
            raise Exception("Too many errors!")
    return [
        livefeed_flightdata_dict(lfr)
        for r in results
        if isinstance(r, bytes)
        for lfr in livefeed_playback_response_parse(r).flights_list
    ]
