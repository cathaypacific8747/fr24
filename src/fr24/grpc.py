"""
Endpoint: https://data-feed.flightradar24.com

Service name: fr24.feed.api.v1.Feed

Methods:

- `LiveFeed`
- `Playback`
- `NearestFlights`
- `LiveFlightsStatus`
- `FollowFlight`
- `TopFlights`
- `LiveTrail`
"""

from __future__ import annotations

import asyncio
from typing import Any, AsyncIterator, Type

import httpx
from google.protobuf.field_mask_pb2 import FieldMask

from .logging import logger
from .proto import T, encode_message, parse_data
from .proto.headers import get_headers
from .proto.v1_pb2 import (
    FetchSearchIndexRequest,
    FetchSearchIndexResponse,
    Flight,
    FollowFlightRequest,
    FollowFlightResponse,
    HistoricTrailRequest,
    HistoricTrailResponse,
    LiveFeedRequest,
    LiveFeedResponse,
    LiveFlightsStatusRequest,
    LiveFlightsStatusResponse,
    LiveTrailRequest,
    LiveTrailResponse,
    LocationBoundaries,
    NearestFlightsRequest,
    NearestFlightsResponse,
    PlaybackRequest,
    PlaybackResponse,
    PositionBuffer,
    RestrictionVisibility,
    TopFlightsRequest,
    TopFlightsResponse,
    TrafficType,
    VisibilitySettings,
)
from .static.bbox import lng_bounds
from .types.authentication import Authentication
from .types.cache import LiveFeed, RecentPosition
from .types.fr24 import LiveFeedField


def construct_request(
    method_name: str,
    message: T,
    auth: None | Authentication = None,
) -> httpx.Request:
    """Construct the gRPC request with encoded gRPC body."""
    return httpx.Request(
        "POST",
        f"https://data-feed.flightradar24.com/fr24.feed.api.v1.Feed/{method_name}",
        headers=get_headers(auth),
        content=encode_message(message),
    )


async def post_unary(
    client: httpx.AsyncClient, request: httpx.Request, msg_type: Type[T]
) -> T:
    """Execute the unary-unary call and return the parsed protobuf message."""
    response = await client.send(request)
    data = response.content
    return parse_data(data, msg_type)


async def post_stream(
    client: httpx.AsyncClient, request: httpx.Request, msg_type: Type[T]
) -> AsyncIterator[T]:
    """Execute the unary-stream call and yield each parsed protobuf message."""
    response = await client.send(request, stream=True)
    try:
        async for chunk in response.aiter_bytes():
            yield parse_data(chunk, msg_type)
    finally:
        await response.aclose()


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

    :param north: North latitude (degrees)
    :param south: South latitude (degrees)
    :param west: West longitude (degrees)
    :param east: East longitude (degrees)
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


def live_feed_request_create(
    message: LiveFeedRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("LiveFeed", message, auth)


async def live_feed_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveFeedResponse:
    return await post_unary(client, request, LiveFeedResponse)


# TODO: this is redundant, deprecate this since the generated pyi now has docs
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


def live_feed_playback_request_create(
    message: PlaybackRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("Playback", message, auth)


async def live_feed_playback_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> PlaybackResponse:
    return await post_unary(client, request, PlaybackResponse)


def live_feed_position_buffer_dict(
    position_buffer: PositionBuffer,
) -> list[RecentPosition]:
    return [
        {
            "delta_lat": pb.delta_lat,
            "delta_lon": pb.delta_lon,
            "delta_ms": pb.delta_ms,
        }
        for pb in position_buffer.recent_positions_list
    ]


def live_feed_flightdata_dict(
    lfr: Flight,
) -> LiveFeed:
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
        "position_buffer": live_feed_position_buffer_dict(lfr.position_buffer),
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
) -> list[LiveFeed]:
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
) -> list[LiveFeed]:
    """
    Retrieve live feed playback data for the entire world, in chunks.

    NOTE: playback data has no position buffer information.

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


def nearest_flights_request_create(
    message: NearestFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("NearestFlights", message, auth)


async def nearest_flights_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> NearestFlightsResponse:
    return await post_unary(client, request, NearestFlightsResponse)


def live_flights_status_request_create(
    message: LiveFlightsStatusRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("LiveFlightsStatus", message, auth)


async def live_flights_status_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveFlightsStatusResponse:
    return await post_unary(client, request, LiveFlightsStatusResponse)


def _search_index_request_create(
    message: FetchSearchIndexRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("FetchSearchIndex", message, auth)


async def _search_index_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> FetchSearchIndexResponse:
    return await post_unary(client, request, FetchSearchIndexResponse)


def follow_flight_request_create(
    message: FollowFlightRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("FollowFlight", message, auth)


async def follow_flight_stream(
    client: httpx.AsyncClient, request: httpx.Request
) -> AsyncIterator[FollowFlightResponse]:
    async for msg in post_stream(client, request, FollowFlightResponse):
        yield msg


def top_flights_request_create(
    message: TopFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("TopFlights", message, auth)


async def top_flights_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> TopFlightsResponse:
    return await post_unary(client, request, TopFlightsResponse)


def live_trail_request_create(
    message: LiveTrailRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    """WARN: Unstable API - does not return data reliably."""
    return construct_request("LiveTrail", message, auth)


async def live_trail_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> LiveTrailResponse:
    """WARN: Unstable API - does not return data reliably."""
    return await post_unary(client, request, LiveTrailResponse)


def _historic_trail_request_create(
    message: HistoricTrailRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("HistoricTrail", message, auth)


async def _historic_trail_post(
    client: httpx.AsyncClient, request: httpx.Request
) -> HistoricTrailResponse:
    return await post_unary(client, request, HistoricTrailResponse)
