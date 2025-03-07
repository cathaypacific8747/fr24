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

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NamedTuple, Union, cast, overload

import httpx
from google.protobuf.field_mask_pb2 import FieldMask
from typing_extensions import override

from .proto import (
    ProtoError,
    SupportsToProto,
    T,
    encode_message,
    parse_data,
    to_proto,
)
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
from .static.bbox import LNGS_WORLD_STATIC
from .utils import Result, get_current_timestamp, to_unix_timestamp

if TYPE_CHECKING:
    from datetime import datetime
    from typing import Annotated, AsyncGenerator, Literal, Type

    import polars as pl
    from typing_extensions import TypeAlias

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


# NOTE: overload not used for now.
@overload
async def post_unary(
    client: httpx.AsyncClient,
    request: httpx.Request,
    msg_type: Type[T],
) -> Result[T, ProtoError]: ...


@overload
async def post_unary(
    client: httpx.AsyncClient,
    request: httpx.Request,
    msg_type: None = None,
) -> httpx.Response: ...


async def post_unary(
    client: httpx.AsyncClient,
    request: httpx.Request,
    msg_type: Type[T] | None = None,
) -> Result[T, ProtoError] | httpx.Response:
    """
    Execute the unary-unary call.

    :param msg_type: The protobuf message type to parse the response into.
    If `None`, the raw httpx response is returned.
    """
    response = await client.send(request)
    if msg_type is None:
        return response
    data = response.content
    return parse_data(data, msg_type)


# TODO: make parsing optional.
async def post_stream(
    client: httpx.AsyncClient,
    request: httpx.Request,
    msg_type: Type[T],
) -> AsyncGenerator[Result[T, ProtoError]]:
    """
    Execute the unary-stream call, yielding each parsed response.
    """
    response = await client.send(request, stream=True)
    try:
        async for chunk in response.aiter_bytes():
            yield parse_data(chunk, msg_type)
    finally:
        await response.aclose()


#
# live feed
#


LiveFeedRequestLike: TypeAlias = Union[
    SupportsToProto[LiveFeedRequest], LiveFeedRequest
]


def live_feed_request_create(
    message_like: LiveFeedRequestLike,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("LiveFeed", to_proto(message_like), auth)


class BoundingBox(NamedTuple):
    south: float
    """Latitude, minimum, degrees"""
    north: float
    """Latitude, maximum, degrees"""
    west: float
    """Longitude, minimum, degrees"""
    east: float
    """Longitude, maximum, degrees"""


BBOXES_WORLD_STATIC = [
    BoundingBox(-90, 90, LNGS_WORLD_STATIC[i], LNGS_WORLD_STATIC[i + 1])
    for i in range(len(LNGS_WORLD_STATIC) - 1)
]
"""Default static bounding boxes covering the entire world"""

BBOX_FRANCE_UIR = BoundingBox(42, 52, -8, 10)
"""Bounding box for france UIR"""


@dataclass
class LiveFeedParams(SupportsToProto[LiveFeedRequest]):
    bounding_box: BoundingBox = BBOX_FRANCE_UIR
    stats: bool = False
    """Whether to include stats in the given area."""
    limit: int = 1500
    """
    Maximum number of flights (should be set to 1500 for unauthorized users,
    2000 for authorized users).
    """
    maxage: int = 14400
    """Maximum time since last message update, seconds."""
    fields: set[LiveFeedField] = field(
        default_factory=lambda: {"flight", "reg", "route", "type"}
    )
    """
    Fields to include.

    For unauthenticated users, a maximum of 4 fields can be included.
    When authenticated, `squawk`, `vspeed`, `airspace`, `logo_id` and `age`
    can be included.
    """

    def to_proto(self) -> LiveFeedRequest:
        return LiveFeedRequest(
            bounds=LocationBoundaries(
                north=self.bounding_box.north,
                south=self.bounding_box.south,
                west=self.bounding_box.west,
                east=self.bounding_box.east,
            ),
            settings=VisibilitySettings(
                sources_list=range(10),  # type: ignore
                services_list=range(12),  # type: ignore
                traffic_type=TrafficType.ALL,
                only_restricted=False,
            ),
            field_mask=FieldMask(paths=self.fields),
            highlight_mode=False,
            stats=self.stats,
            limit=self.limit,
            maxage=self.maxage,
            restriction_mode=RestrictionVisibility.NOT_VISIBLE,
        )


# TODO: add typing.overload for return type
async def live_feed(
    client: httpx.AsyncClient,
    message_like: LiveFeedRequestLike,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, LiveFeedResponse]:
    response = await client.send(live_feed_request_create(message_like, auth))
    return response


def live_feed_parse(
    response: Annotated[httpx.Response, LiveFeedResponse],
) -> Result[LiveFeedResponse, ProtoError]:
    return parse_data(response.content, LiveFeedResponse)


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


def live_feed_flightdata_dict(lfr: Flight) -> LiveFeed:
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


def live_feed_df(
    data: LiveFeedResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import live_feed_schema

    return pl.DataFrame(
        (live_feed_flightdata_dict(lfr) for lfr in data.flights_list),
        schema=live_feed_schema,
    )


#
# live feed playback
#


# TODO: refactor to allow more flexible timestamps
# NOTE: composition would be better,
# but we want a flat structure in the service API and avoid rewriting __init__
@dataclass
class LiveFeedPlaybackParams(LiveFeedParams, SupportsToProto[PlaybackRequest]):
    timestamp: int | datetime | Literal["now"] = "now"
    """Start timestamp"""
    duration: int = 7
    """
    Duration of prefetch, `floor(7.5*(multiplier))` seconds

    For 1x playback, this should be 7 seconds.
    """
    hfreq: int | None = None
    """High frequency mode"""

    @override
    def to_proto(self) -> PlaybackRequest:  # type: ignore
        timestamp = to_unix_timestamp(self.timestamp)
        if timestamp == "now":
            timestamp = get_current_timestamp() - self.duration
        # timestamp should not be None, silence mypy
        timestamp = cast(int, timestamp)
        return PlaybackRequest(
            live_feed_request=super().to_proto(),
            timestamp=timestamp,
            prefetch=timestamp + self.duration,
            hfreq=self.hfreq,
        )


PlaybackRequestLike: TypeAlias = Union[
    SupportsToProto[PlaybackRequest], PlaybackRequest, LiveFeedPlaybackParams
]


def live_feed_playback_request_create(
    message_like: PlaybackRequestLike,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("Playback", to_proto(message_like), auth)


async def live_feed_playback(
    client: httpx.AsyncClient,
    message_like: PlaybackRequestLike,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, LiveFeedResponse]:
    response = await client.send(
        live_feed_playback_request_create(message_like, auth)
    )
    return response


def live_feed_playback_parse(
    response: Annotated[httpx.Response, PlaybackResponse],
) -> Result[PlaybackResponse, ProtoError]:
    return parse_data(response.content, PlaybackResponse)


def live_feed_playback_df(
    data: PlaybackResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import live_feed_schema

    return pl.DataFrame(
        (
            live_feed_flightdata_dict(lfr)
            for lfr in data.live_feed_response.flights_list
        ),
        schema=live_feed_schema,
    )


#
# misc
#


def nearest_flights_request_create(
    message: NearestFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("NearestFlights", message, auth)


async def nearest_flights(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[NearestFlightsResponse, ProtoError]:
    return await post_unary(client, request, NearestFlightsResponse)


def live_flights_status_request_create(
    message: LiveFlightsStatusRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("LiveFlightsStatus", message, auth)


async def live_flights_status(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[LiveFlightsStatusResponse, ProtoError]:
    return await post_unary(client, request, LiveFlightsStatusResponse)


def search_index_request_create(
    message: FetchSearchIndexRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("FetchSearchIndex", message, auth)


async def search_index(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[FetchSearchIndexResponse, ProtoError]:
    """WARN: Unstable API - does not return data reliably."""
    return await post_unary(client, request, FetchSearchIndexResponse)


def follow_flight_request_create(
    message: FollowFlightRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("FollowFlight", message, auth)


async def follow_flight_stream(
    client: httpx.AsyncClient, request: httpx.Request
) -> AsyncGenerator[Result[FollowFlightResponse, ProtoError]]:
    async for msg in post_stream(client, request, FollowFlightResponse):
        yield msg


def top_flights_request_create(
    message: TopFlightsRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("TopFlights", message, auth)


async def top_flights(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[TopFlightsResponse, ProtoError]:
    return await post_unary(client, request, TopFlightsResponse)


def live_trail_request_create(
    message: LiveTrailRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("LiveTrail", message, auth)


async def live_trail(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[LiveTrailResponse, ProtoError]:
    """WARN: Unstable API - does not return data reliably."""
    return await post_unary(client, request, LiveTrailResponse)


def historic_trail_request_create(
    message: HistoricTrailRequest,
    auth: None | Authentication = None,
) -> httpx.Request:
    return construct_request("HistoricTrail", message, auth)


async def historic_trail(
    client: httpx.AsyncClient, request: httpx.Request
) -> Result[HistoricTrailResponse, ProtoError]:
    """WARN: Unstable API - does not return data reliably."""
    # empty DATA frame
    return await post_unary(client, request, HistoricTrailResponse)


__all__ = [
    "BoundingBox",
]
