from __future__ import annotations

import asyncio
from typing import Any

import httpx
from google.protobuf.field_mask_pb2 import FieldMask
from loguru import logger

from .proto import encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    Flight,
    LiveFeedRequest,
    LiveFeedResponse,
    LocationBoundaries,
    PlaybackRequest,
    PlaybackResponse,
    RestrictionVisibility,
    TrafficType,
    VisibilitySettings,
)
from .static.bbox import lng_bounds
from .types.authentication import Authentication
from .types.cache import LiveFeedRecord
from .types.fr24 import LiveFeedField


def live_feed_message_create(
    north: float = 50,
    south: float = 40,
    west: float = 0,
    east: float = 10,
    stats: bool = False,
    limit: int = 1500,
    maxage: int = 14400,
    fields: list[LiveFeedField] = [
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
    :param limit: Max number of flights (default 1500 for unauthenticated users,
        2000 for authenticated users)
    :param maxage: Max age since last update, seconds
    :param fields: fields to include - for unauthenticated users, max 4 fields.
        When authenticated, `squawk`, `vspeed`, `airspace`, `logo_id` and `age`
        can be included
    """
    return LiveFeedRequest(
        bounds=LocationBoundaries(
            north=north, south=south, west=west, east=east
        ),
        settings=VisibilitySettings(
            sources_list=range(10),  # type: ignore
            services_list=range(12),  # type: ignore
            traffic_type=TrafficType.ALL,
            only_restricted=False,
        ),
        field_mask=FieldMask(paths=fields),
        highlight_mode=False,
        stats=stats,
        limit=limit,
        maxage=maxage,
        restriction_mode=RestrictionVisibility.NOT_VISIBLE,
        **kwargs,
    )


def live_feed_playback_message_create(
    message: LiveFeedRequest,
    timestamp: int,
    prefetch: int,
    hfreq: int,
) -> PlaybackRequest:
    """
    Create the live feed playback request protobuf message.

    :param timestamp: Start timestamp
    :param prefetch: End timestamp: should be start timestamp + 7 seconds
    :param hfreq: High frequency mode
    """
    return PlaybackRequest(
        live_feed_request=message,
        timestamp=timestamp,
        prefetch=prefetch,
        hfreq=hfreq,
    )


def live_feed_request_create(
    message: LiveFeedRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/LiveFeed",
        headers=get_headers(auth),
        content=encode_message(message),
    )


def live_feed_playback_request_create(
    message: PlaybackRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Constructs the POST request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        "https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/Playback",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def live_feed_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveFeedResponse:
    """Send the request and parse the protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, LiveFeedResponse)


async def live_feed_playback_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> PlaybackResponse:
    """Send the request and parse raw protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, PlaybackResponse)


def live_feed_flightdata_dict(
    lfr: Flight,
) -> LiveFeedRecord:
    """Convert the protobuf message to a dictionary."""
    return {
        "timestamp": lfr.timestamp,
        "flightid": lfr.flightid,
        "latitude": lfr.lat,
        "longitude": lfr.lon,
        "track": lfr.track,
        "altitude": lfr.alt,
        "ground_speed": lfr.speed,
        "vertical_speed": lfr.extra_info.vspeed,
        "on_ground": lfr.on_ground,
        "callsign": lfr.callsign,
        "source": lfr.source,
        "registration": lfr.extra_info.reg,
        "origin": getattr(lfr.extra_info.route, "from"),
        "destination": lfr.extra_info.route.to,
        "typecode": lfr.extra_info.type,
        "eta": lfr.extra_info.schedule.eta,
        "squawk": lfr.extra_info.squawk,
    }


# N, S, W, E
world_zones = [
    (90, -90, lng_bounds[i], lng_bounds[i + 1])
    for i in range(len(lng_bounds) - 1)
]


# TODO: add parameter for custom bounds, e.g. from .bounds.lng_bounds_per_30_min
async def live_feed_world_data(
    client: httpx.AsyncClient,
    auth: None | Authentication = None,
    limit: int = 1500,
    fields: list[LiveFeedField] = [
        "flight",
        "reg",
        "route",
        "type",
    ],
) -> list[LiveFeedRecord]:
    """Retrieve live feed data for the entire world, in chunks."""
    results = await asyncio.gather(
        *[
            live_feed_post(
                client,
                live_feed_request_create(
                    live_feed_message_create(
                        *bounds, limit=limit, fields=fields
                    ),
                    auth=auth,
                ),
            )
            for bounds in world_zones
        ],
        return_exceptions=True,
    )
    return [
        live_feed_flightdata_dict(lfr)
        for r in results
        if not isinstance(r, BaseException)
        for lfr in r.flights_list
    ]


async def live_feed_playback_world_data(
    client: httpx.AsyncClient,
    timestamp: int,
    duration: int = 7,
    hfreq: int = 0,
    auth: None | Authentication = None,
    limit: int = 1500,
    fields: list[LiveFeedField] = [
        "flight",
        "reg",
        "route",
        "type",
    ],
) -> list[LiveFeedRecord]:
    """
    Retrieve live feed playback data for the entire world, in chunks.

    :raises RuntimeError: if more than half of the requests fail
    """
    results = await asyncio.gather(
        *[
            live_feed_playback_post(
                client,
                live_feed_playback_request_create(
                    live_feed_playback_message_create(
                        live_feed_message_create(
                            *bounds, limit=limit, fields=fields
                        ),
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
    if len(err := [r for r in results if isinstance(r, BaseException)]) > 0:
        logger.warning(f"{len(err)} errors: {err}!")
        if len(err) > len(results) / 2:
            raise RuntimeError(
                f"playback world: found {len(err)} errors, aborting!"
            )
    return [
        live_feed_flightdata_dict(lfr)
        for r in results
        if not isinstance(r, BaseException)
        for lfr in r.live_feed_response.flights_list
    ]
