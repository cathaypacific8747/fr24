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
- ~~`HistoricTrail`~~
- ~~`FetchSearchIndex`~~
- `FlightDetails`
- `PlaybackFlight`

"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, NamedTuple, Sequence, Union, cast, overload

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
    EMSInfo,
    FetchSearchIndexRequest,
    FetchSearchIndexResponse,
    Flight,
    FlightDetailsRequest,
    FlightDetailsResponse,
    FollowedFlight,
    FollowFlightRequest,
    FollowFlightResponse,
    Geolocation,
    HistoricTrailRequest,
    HistoricTrailResponse,
    LiveFeedRequest,
    LiveFeedResponse,
    LiveFlightsStatusRequest,
    LiveFlightsStatusResponse,
    LiveFlightStatus,
    LiveTrailRequest,
    LiveTrailResponse,
    LocationBoundaries,
    NearbyFlight,
    NearestFlightsRequest,
    NearestFlightsResponse,
    PlaybackFlightRequest,
    PlaybackFlightResponse,
    PlaybackRequest,
    PlaybackResponse,
    PositionBuffer,
    RestrictionVisibility,
    TopFlightsRequest,
    TopFlightsResponse,
    TrafficType,
    TrailPoint,
    VisibilitySettings,
)
from .static.bbox import LNGS_WORLD_STATIC
from .utils import (
    Result,
    get_current_timestamp,
    to_flight_id,
    to_unix_timestamp,
)

if TYPE_CHECKING:
    from typing import Annotated, AsyncGenerator, Literal, Type

    import polars as pl
    from google.protobuf.internal.enum_type_wrapper import _V, _EnumTypeWrapper
    from typing_extensions import TypeAlias

    from .types.authentication import Authentication
    from .types.cache import (
        EMSRecord,
        FlightDetailsRecord,
        FlightRecord,
        LiveFlightStatusRecord,
        NearbyFlightRecord,
        PlaybackFlightRecord,
        RecentPositionRecord,
        TopFlightRecord,
        TrailPointRecord,
    )
    from .types.fr24 import LiveFeedField
    from .utils import IntoFlightId, IntoTimestamp

#
# helpers
#


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


def to_protobuf_enum(
    enum: _V | str | bytes,
    type_wrapper: _EnumTypeWrapper[_V],
) -> _V:
    if isinstance(enum, (str, bytes)):
        return type_wrapper.Value(enum)
    return enum


#
# live feed
#


IntoLiveFeedRequest: TypeAlias = Union[
    SupportsToProto[LiveFeedRequest], LiveFeedRequest
]


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
    """Maximum number of flights (should be set to 1500 for unauthorized users,
    2000 for authorized users).
    """
    maxage: int = 14400
    """Maximum time since last message update, seconds."""
    fields: set[LiveFeedField] = field(
        default_factory=lambda: {"flight", "reg", "route", "type"}
    )
    """Fields to include.

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
    message: IntoLiveFeedRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, LiveFeedResponse]:
    request = construct_request("LiveFeed", to_proto(message), auth)
    response = await client.send(request)
    return response


def live_feed_position_buffer_dict(
    position_buffer: PositionBuffer,
) -> list[RecentPositionRecord]:
    return [
        {
            "delta_lat": pb.delta_lat,
            "delta_lon": pb.delta_lon,
            "delta_ms": pb.delta_ms,
        }
        for pb in position_buffer.recent_positions_list
    ]


def live_feed_flightdata_dict(lfr: Flight) -> FlightRecord:
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
    timestamp: IntoTimestamp | Literal["now"] = "now"
    """Start timestamp"""
    duration: int = 7
    """Duration of prefetch, `floor(7.5*(multiplier))` seconds

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


IntoPlaybackRequest: TypeAlias = Union[
    SupportsToProto[PlaybackRequest], PlaybackRequest, LiveFeedPlaybackParams
]


async def live_feed_playback(
    client: httpx.AsyncClient,
    message: IntoPlaybackRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, LiveFeedResponse]:
    request = construct_request("Playback", to_proto(message), auth)
    response = await client.send(request)
    return response


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


IntoNearestFlightsRequest: TypeAlias = Union[
    SupportsToProto[NearestFlightsRequest], NearestFlightsRequest
]


@dataclass
class NearestFlightsParams(SupportsToProto[NearestFlightsRequest]):
    lat: float
    """Latitude, degrees, -90 to 90"""
    lon: float
    """Longitude, degrees, -180 to 180"""
    radius: int = 10000
    """Radius, metres"""
    limit: int = 1500
    """Maximum number of aircraft to return"""

    def to_proto(self) -> NearestFlightsRequest:
        return NearestFlightsRequest(
            location=Geolocation(lat=self.lat, lon=self.lon),
            radius=self.radius,
            limit=self.limit,
        )


async def nearest_flights(
    client: httpx.AsyncClient,
    message: IntoNearestFlightsRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, NearestFlightsResponse]:
    request = construct_request("NearestFlights", to_proto(message), auth)
    response = await client.send(request)
    return response


IntoLiveFlightsStatusRequest: TypeAlias = Union[
    SupportsToProto[LiveFlightsStatusRequest], LiveFlightsStatusRequest
]


def nearest_flights_nearbyflight_dict(nf: NearbyFlight) -> NearbyFlightRecord:
    return {
        **live_feed_flightdata_dict(nf.flight),
        "distance": nf.distance,
    }


def nearest_flights_df(
    data: NearestFlightsResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import nearest_flights_schema

    return pl.DataFrame(
        (nearest_flights_nearbyflight_dict(nf) for nf in data.flights_list),
        schema=nearest_flights_schema,
    )


@dataclass
class LiveFlightsStatusParams(SupportsToProto[LiveFlightsStatusRequest]):
    flight_ids: Sequence[IntoFlightId]
    """List of flight IDs to get status for"""

    def to_proto(self) -> LiveFlightsStatusRequest:
        return LiveFlightsStatusRequest(
            flight_ids_list=tuple(to_flight_id(fid) for fid in self.flight_ids)
        )


async def live_flights_status(
    client: httpx.AsyncClient,
    message: IntoLiveFlightsStatusRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, LiveFlightsStatusResponse]:
    request = construct_request("LiveFlightsStatus", to_proto(message), auth)
    response = await client.send(request)
    return response


def live_flights_status_flightstatusdata_dict(
    flight_status: LiveFlightStatus,
) -> LiveFlightStatusRecord:
    data = flight_status.data

    return {
        "flight_id": flight_status.flight_id,
        "latitude": data.lat,
        "longitude": data.lon,
        "status": data.status,
        "squawk": data.squawk,
    }


def live_flights_status_df(
    data: LiveFlightsStatusResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import live_flights_status_schema

    return pl.DataFrame(
        (
            live_flights_status_flightstatusdata_dict(fs)
            for fs in data.flights_map
        ),
        schema=live_flights_status_schema,
    )


IntoFetchSearchIndexRequest: TypeAlias = Union[
    SupportsToProto[FetchSearchIndexRequest], FetchSearchIndexRequest
]


async def search_index(
    client: httpx.AsyncClient,
    message: IntoFetchSearchIndexRequest,
    auth: None | Authentication = None,
) -> Result[FetchSearchIndexResponse, ProtoError]:
    """WARN: Unstable API - does not return data reliably."""
    request = construct_request("FetchSearchIndex", to_proto(message), auth)
    return await post_unary(client, request, FetchSearchIndexResponse)


IntoFollowFlightRequest: TypeAlias = Union[
    SupportsToProto[FollowFlightRequest], FollowFlightRequest
]


async def follow_flight_stream(
    client: httpx.AsyncClient,
    message: IntoFollowFlightRequest,
    auth: None | Authentication = None,
) -> AsyncGenerator[Result[FollowFlightResponse, ProtoError]]:
    request = construct_request("FollowFlight", to_proto(message), auth)
    async for msg in post_stream(client, request, FollowFlightResponse):
        yield msg


@dataclass
class TopFlightsParams(SupportsToProto[TopFlightsRequest]):
    limit: int = 10
    """Maximum number of top flights to return (1-10)"""

    def to_proto(self) -> TopFlightsRequest:
        return TopFlightsRequest(limit=self.limit)


IntoTopFlightsRequest: TypeAlias = Union[
    SupportsToProto[TopFlightsRequest], TopFlightsRequest
]


async def top_flights(
    client: httpx.AsyncClient,
    message: IntoTopFlightsRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, TopFlightsResponse]:
    request = construct_request("TopFlights", to_proto(message), auth)
    response = await client.send(request)
    return response


def top_flights_dict(ff: FollowedFlight) -> TopFlightRecord:
    return {
        "flight_id": ff.flight_id,
        "live_clicks": ff.live_clicks,
        "total_clicks": ff.total_clicks,
        "flight_number": ff.flight_number,
        "callsign": ff.callsign,
        "squawk": ff.squawk,
        "from_iata": ff.from_iata,
        "from_city": ff.from_city,
        "to_iata": ff.to_iata,
        "to_city": ff.to_city,
        "type": ff.type,
        "full_description": ff.full_description,
    }


def top_flights_df(data: TopFlightsResponse) -> pl.DataFrame:
    import polars as pl

    from .types.cache import top_flights_schema

    return pl.DataFrame(
        (top_flights_dict(ff) for ff in data.scoreboard_list),
        schema=top_flights_schema,
    )


IntoLiveTrailRequest: TypeAlias = Union[
    SupportsToProto[LiveTrailRequest], LiveTrailRequest
]


async def live_trail(
    client: httpx.AsyncClient,
    message: IntoLiveTrailRequest,
    auth: None | Authentication = None,
) -> Result[LiveTrailResponse, ProtoError]:
    """WARN: Unstable API - does not return data reliably.
    contains empty `DATA` frame error if flight_id is not live"""
    request = construct_request("LiveTrail", to_proto(message), auth)
    return await post_unary(client, request, LiveTrailResponse)


IntoHistoricTrailRequest: TypeAlias = Union[
    SupportsToProto[HistoricTrailRequest], HistoricTrailRequest
]


async def historic_trail(
    client: httpx.AsyncClient,
    message: IntoHistoricTrailRequest,
    auth: None | Authentication = None,
) -> Result[HistoricTrailResponse, ProtoError]:
    """WARN: Unstable API - returns empty `DATA` frame."""
    request = construct_request("HistoricTrail", to_proto(message), auth)
    return await post_unary(client, request, HistoricTrailResponse)


IntoFlightDetailsRequest: TypeAlias = Union[
    SupportsToProto[FlightDetailsRequest], FlightDetailsRequest
]


@dataclass
class FlightDetailsParams(SupportsToProto[FlightDetailsRequest]):
    flight_id: IntoFlightId
    """Flight ID to fetch details for.
    Must be live, or the response will contain an empty `DATA` frame error."""
    restriction_mode: RestrictionVisibility.ValueType | str | bytes = (
        RestrictionVisibility.NOT_VISIBLE
    )
    """[FAA LADD](https://www.faa.gov/pilots/ladd) visibility mode."""
    verbose: bool = True
    """Whether to include [fr24.proto.v1_pb2.FlightDetailsResponse.flight_plan]
    and [fr24.proto.v1_pb2.FlightDetailsResponse.aircraft_details] in the
    response."""

    def to_proto(self) -> FlightDetailsRequest:
        return FlightDetailsRequest(
            flight_id=to_flight_id(self.flight_id),
            restriction_mode=to_protobuf_enum(
                self.restriction_mode, RestrictionVisibility
            ),
            verbose=self.verbose,
        )


async def flight_details(
    client: httpx.AsyncClient,
    message: IntoFlightDetailsRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, FlightDetailsResponse]:
    """contains empty `DATA` frame error if flight_id is not live"""
    request = construct_request("FlightDetails", to_proto(message), auth)
    response = await client.send(request)
    return response


def flight_details_dict(
    response: FlightDetailsResponse,
) -> FlightDetailsRecord:
    aircraft_info = response.aircraft_info
    schedule_info = response.schedule_info
    flight_progress = response.flight_progress
    flight_info = response.flight_info

    return {
        # aircraft info
        "icao_address": aircraft_info.icao_address,
        "reg": aircraft_info.reg,
        "typecode": aircraft_info.type,
        # schedule info
        "flight_number": schedule_info.flight_number,
        "origin_id": schedule_info.origin_id,
        "destination_id": schedule_info.destination_id,
        "diverted_id": schedule_info.diverted_to_id,
        "scheduled_departure": schedule_info.scheduled_departure,
        "scheduled_arrival": schedule_info.scheduled_arrival,
        "actual_departure": schedule_info.actual_departure,
        "actual_arrival": schedule_info.actual_arrival,
        # flight progress
        "traversed_distance": flight_progress.traversed_distance,
        "remaining_distance": flight_progress.remaining_distance,
        "elapsed_time": flight_progress.elapsed_time,
        "remaining_time": flight_progress.remaining_time,
        "eta": flight_progress.eta,
        "great_circle_distance": flight_progress.great_circle_distance,
        "mean_flight_time": flight_progress.mean_flight_time,
        # flight info
        "timestamp_ms": flight_info.timestamp_ms,
        "flightid": flight_info.flightid,
        "latitude": flight_info.lat,
        "longitude": flight_info.lon,
        "track": flight_info.track,
        "altitude": flight_info.alt,
        "ground_speed": flight_info.speed,
        "vertical_speed": flight_info.vspeed,
        "on_ground": flight_info.on_ground,
        "callsign": flight_info.callsign,
        "squawk": flight_info.squawk,
        "ems": ems_dict(flight_info.ems_info),
        # TODO: add flight plan
        "flight_trail_list": [
            trail_point_dict(tp) for tp in response.flight_trail_list
        ],
    }


def trail_point_dict(tp: TrailPoint) -> TrailPointRecord:
    return {
        "timestamp": tp.snapshot_id,
        "latitude": tp.lat,
        "longitude": tp.lon,
        "altitude": tp.altitude,
        "ground_speed": tp.spd,
        "track": tp.heading,
        "vertical_speed": tp.vspd,
    }


def ems_dict(ems: EMSInfo) -> EMSRecord:
    """Transform Enhanced Mode-S data in the protobuf message into a dictionary.

    This is similar to EMS data in the [JSON API response][fr24.json.playback],
    specifically [fr24.json.playback_track_ems_dict][], which gets converted to
    [fr24.types.cache.PlaybackTrackEMSRecord][]. However, several fields are
    missing:

    - `timestamp`
    - `autopilot`
    - `track`
    - `roll`
    - `precision`
    - `emergency`
    - `tcas_acas`
    - `heading`
    """
    return {
        "ias": ems.ias,
        "tas": ems.tas,
        "mach": ems.mach,
        "mcp": ems.amcp,
        "fms": ems.afms,
        "oat": ems.oat,
        "qnh": ems.qnh,
        "wind_dir": ems.wind_dir,
        "wind_speed": ems.wind_speed,
        "altitude_gps": ems.agps,
        "agpsdiff": ems.agpsdiff,
        "apflags": ems.apflags,
        "rs": ems.rs,
    }


def flight_details_df(
    data: FlightDetailsResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import flight_details_schema

    return pl.DataFrame(
        [flight_details_dict(data)],
        schema=flight_details_schema,
    )


IntoPlaybackFlightRequest: TypeAlias = Union[
    SupportsToProto[PlaybackFlightRequest], PlaybackFlightRequest
]


@dataclass
class PlaybackFlightParams(SupportsToProto[PlaybackFlightRequest]):
    flight_id: IntoFlightId
    """Flight ID to fetch details for.
    Must not be live, or the response will contain an empty `DATA` frame error.
    """
    timestamp: IntoTimestamp
    """Actual time of departure (ATD) of the historic flight,
    Unix timestamp in seconds."""

    def to_proto(self) -> PlaybackFlightRequest:
        return PlaybackFlightRequest(
            flight_id=to_flight_id(self.flight_id),
            timestamp=to_unix_timestamp(self.timestamp),  # type: ignore
        )


async def playback_flight(
    client: httpx.AsyncClient,
    message: IntoPlaybackFlightRequest,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, PlaybackFlightResponse]:
    """contains empty `DATA` frame error if flight_id is live"""
    request = construct_request("PlaybackFlight", to_proto(message), auth)
    response = await client.send(request)
    return response


def playback_flight_dict(
    response: PlaybackFlightResponse,
) -> PlaybackFlightRecord:
    aircraft_info = response.aircraft_info
    schedule_info = response.schedule_info
    flight_info = response.flight_info

    return {
        # aircraft info
        "icao_address": aircraft_info.icao_address,
        "reg": aircraft_info.reg,
        "typecode": aircraft_info.type,
        # schedule info
        "flight_number": schedule_info.flight_number,
        "origin_id": schedule_info.origin_id,
        "destination_id": schedule_info.destination_id,
        "diverted_id": schedule_info.diverted_to_id,
        "scheduled_departure": schedule_info.scheduled_departure,
        "scheduled_arrival": schedule_info.scheduled_arrival,
        "actual_departure": schedule_info.actual_departure,
        "actual_arrival": schedule_info.actual_arrival,
        # flight info
        "timestamp_ms": flight_info.timestamp_ms,
        "flightid": flight_info.flightid,
        "latitude": flight_info.lat,
        "longitude": flight_info.lon,
        "track": flight_info.track,
        "altitude": flight_info.alt,
        "ground_speed": flight_info.speed,
        "vertical_speed": flight_info.vspeed,
        "on_ground": flight_info.on_ground,
        "callsign": flight_info.callsign,
        "squawk": flight_info.squawk,
        "ems": ems_dict(flight_info.ems_info),
        # flight trail
        "flight_trail_list": [
            trail_point_dict(tp) for tp in response.flight_trail_list
        ],
    }


def playback_flight_df(
    data: PlaybackFlightResponse,
) -> pl.DataFrame:
    import polars as pl

    from .types.cache import playback_flight_schema

    return pl.DataFrame(
        [playback_flight_dict(data)],
        schema=playback_flight_schema,
    )


__all__ = ["BoundingBox"]
