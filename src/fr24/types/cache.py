from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Any, get_type_hints

import polars as pl
from typing_extensions import TypedDict

# NOTE: Parquet does not support timestamp in seconds:
# https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#timestamp
# using u32 or timestamp_ms for now


@dataclass(frozen=True)
class DType:
    """A newtype for annotating types in TypedDicts."""

    type_: pl.DataType

    def __post_init__(self) -> None:
        assert isinstance(self.type_, pl.DataType), (
            f"found `{type(self.type_)=}`"
        )


def to_schema(obj: type[Any]) -> dict[str, pl.DataType]:
    """Generate a polars schema from a TypedDict.

    :param obj: A TypedDict with types annotated with `DType`.
    """
    schema = {}
    hints = get_type_hints(obj, include_extras=True)
    for field_name, type_ in hints.items():
        metadata_list = getattr(type_, "__metadata__", None)
        assert metadata_list is not None, (
            f"expected {field_name=} to be `Annotated`, found `{type_}`"
        )
        dtype = None
        for metadata in metadata_list:
            if isinstance(metadata, DType):
                if dtype is not None:
                    raise ValueError(
                        f"multiple `DType` annotations found for {field_name=}"
                    )
                dtype = metadata.type_
        if dtype is None:
            raise ValueError(f"no `DType` found for {field_name=}")
        schema[field_name] = dtype
    return schema


class FlightListRecord(TypedDict):
    flight_id: Annotated[int | None, DType(pl.UInt64())]
    number: Annotated[str | None, DType(pl.String())]
    callsign: Annotated[str | None, DType(pl.String())]
    icao24: Annotated[int | None, DType(pl.UInt32())]
    registration: Annotated[str | None, DType(pl.String())]
    typecode: Annotated[str, DType(pl.String())]
    origin: Annotated[str | None, DType(pl.String())]
    destination: Annotated[str | None, DType(pl.String())]
    status: Annotated[str | None, DType(pl.String())]
    STOD: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]
    ETOD: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]
    ATOD: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]
    STOA: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]
    ETOA: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]
    ATOA: Annotated[int | None, DType(pl.Datetime("ms", time_zone="UTC"))]


flight_list_schema = to_schema(FlightListRecord)


class PlaybackTrackEMSRecord(TypedDict):
    timestamp: Annotated[int, DType(pl.UInt32())]
    ias: Annotated[int | None, DType(pl.Int16())]
    tas: Annotated[int | None, DType(pl.Int16())]
    mach: Annotated[int | None, DType(pl.Int16())]
    mcp: Annotated[int | None, DType(pl.Int32())]
    fms: Annotated[int | None, DType(pl.Int32())]
    autopilot: Annotated[int | None, DType(pl.Int8())]
    oat: Annotated[int | None, DType(pl.Int8())]
    track: Annotated[float | None, DType(pl.Float32())]
    roll: Annotated[float | None, DType(pl.Float32())]
    qnh: Annotated[int | None, DType(pl.UInt16())]
    wind_dir: Annotated[int | None, DType(pl.Int16())]
    wind_speed: Annotated[int | None, DType(pl.Int16())]
    precision: Annotated[int | None, DType(pl.UInt8())]
    altitude_gps: Annotated[int | None, DType(pl.Int32())]
    emergency: Annotated[int | None, DType(pl.UInt8())]
    tcas_acas: Annotated[int | None, DType(pl.UInt8())]
    heading: Annotated[int | None, DType(pl.UInt16())]


playback_track_ems_schema = to_schema(PlaybackTrackEMSRecord)


class PlaybackTrackRecord(TypedDict):
    timestamp: Annotated[int, DType(pl.UInt32())]
    latitude: Annotated[float, DType(pl.Float32())]
    longitude: Annotated[float, DType(pl.Float32())]
    altitude: Annotated[int, DType(pl.Int32())]
    ground_speed: Annotated[int, DType(pl.Int16())]
    vertical_speed: Annotated[int | None, DType(pl.Int16())]
    track: Annotated[int, DType(pl.Int16())]
    squawk: Annotated[int, DType(pl.UInt16())]
    ems: Annotated[
        None | PlaybackTrackEMSRecord,
        DType(pl.Struct(playback_track_ems_schema)),
    ]


playback_track_schema = to_schema(PlaybackTrackRecord)


class RecentPositionRecord(TypedDict):
    delta_lat: Annotated[int, DType(pl.Int32())]
    delta_lon: Annotated[int, DType(pl.Int32())]
    delta_ms: Annotated[int, DType(pl.UInt32())]


position_buffer_struct_schema = to_schema(RecentPositionRecord)


class FlightRecord(TypedDict):
    timestamp: Annotated[int, DType(pl.UInt32())]
    flightid: Annotated[int, DType(pl.UInt32())]
    latitude: Annotated[float, DType(pl.Float32())]
    longitude: Annotated[float, DType(pl.Float32())]
    track: Annotated[int, DType(pl.UInt16())]
    altitude: Annotated[int, DType(pl.Int32())]
    ground_speed: Annotated[int, DType(pl.Int16())]
    on_ground: Annotated[bool, DType(pl.Boolean())]
    callsign: Annotated[str, DType(pl.String())]
    source: Annotated[int, DType(pl.UInt8())]
    registration: Annotated[str, DType(pl.String())]
    origin: Annotated[str, DType(pl.String())]
    destination: Annotated[str, DType(pl.String())]
    typecode: Annotated[str, DType(pl.String())]
    eta: Annotated[int, DType(pl.UInt32())]
    squawk: Annotated[int, DType(pl.UInt16())]
    vertical_speed: Annotated[
        int | None, DType(pl.Int16())
    ]  # 64 * 9-bit + 1-bit sign
    position_buffer: Annotated[
        list[RecentPositionRecord],
        DType(pl.List(pl.Struct(position_buffer_struct_schema))),
    ]


live_feed_schema = to_schema(FlightRecord)


class NearbyFlightRecord(FlightRecord):
    distance: Annotated[int, DType(pl.UInt32())]


nearest_flights_schema = to_schema(NearbyFlightRecord)


class LiveFlightStatusRecord(TypedDict):
    flight_id: Annotated[int, DType(pl.UInt32())]
    latitude: Annotated[float, DType(pl.Float32())]
    longitude: Annotated[float, DType(pl.Float32())]
    status: Annotated[int, DType(pl.UInt8())]
    squawk: Annotated[int, DType(pl.UInt16())]


live_flights_status_schema = to_schema(LiveFlightStatusRecord)


class TopFlightRecord(TypedDict):
    flight_id: Annotated[int, DType(pl.UInt32())]
    live_clicks: Annotated[int, DType(pl.UInt32())]
    total_clicks: Annotated[int, DType(pl.UInt32())]
    flight_number: Annotated[str, DType(pl.String())]
    callsign: Annotated[str, DType(pl.String())]
    squawk: Annotated[int, DType(pl.UInt16())]
    from_iata: Annotated[str, DType(pl.String())]
    from_city: Annotated[str, DType(pl.String())]
    to_iata: Annotated[str, DType(pl.String())]
    to_city: Annotated[str, DType(pl.String())]
    type: Annotated[str, DType(pl.String())]
    full_description: Annotated[str, DType(pl.String())]


top_flights_schema = to_schema(TopFlightRecord)


class EMSRecord(TypedDict):
    ias: Annotated[int | None, DType(pl.Int16())]
    tas: Annotated[int | None, DType(pl.Int16())]
    mach: Annotated[int | None, DType(pl.Int16())]
    mcp: Annotated[int | None, DType(pl.Int32())]
    fms: Annotated[int | None, DType(pl.Int32())]
    oat: Annotated[int | None, DType(pl.Int8())]
    qnh: Annotated[int | None, DType(pl.UInt16())]
    wind_dir: Annotated[int | None, DType(pl.Int16())]
    wind_speed: Annotated[int | None, DType(pl.Int16())]
    altitude_gps: Annotated[int | None, DType(pl.Int32())]
    agpsdiff: Annotated[int | None, DType(pl.Int32())]
    apflags: Annotated[int | None, DType(pl.Int32())]
    rs: Annotated[int | None, DType(pl.Int32())]


ems_struct_schema = to_schema(EMSRecord)


class TrailPointRecord(TypedDict):
    timestamp: Annotated[int, DType(pl.UInt32())]
    latitude: Annotated[float, DType(pl.Float32())]
    longitude: Annotated[float, DType(pl.Float32())]
    altitude: Annotated[int | None, DType(pl.Int32())]
    ground_speed: Annotated[int | None, DType(pl.Int16())]
    track: Annotated[int | None, DType(pl.UInt16())]
    vertical_speed: Annotated[int | None, DType(pl.Int16())]


trail_point_schema = to_schema(TrailPointRecord)


class _AircraftRecord(TypedDict):
    icao_address: Annotated[int, DType(pl.UInt32())]
    reg: Annotated[str, DType(pl.String())]
    typecode: Annotated[str, DType(pl.String())]


class _FlightProgressRecord(TypedDict):
    traversed_distance: Annotated[int, DType(pl.UInt32())]
    remaining_distance: Annotated[int, DType(pl.UInt32())]
    elapsed_time: Annotated[int | None, DType(pl.UInt32())]
    remaining_time: Annotated[int | None, DType(pl.UInt32())]
    eta: Annotated[int, DType(pl.UInt32())]
    great_circle_distance: Annotated[int, DType(pl.UInt32())]
    mean_flight_time: Annotated[int, DType(pl.UInt32())]


class _ScheduleRecord(TypedDict):
    flight_number: Annotated[str, DType(pl.String())]
    origin_id: Annotated[int, DType(pl.UInt32())]
    destination_id: Annotated[int, DType(pl.UInt32())]
    diverted_id: Annotated[int, DType(pl.UInt32())]
    scheduled_departure: Annotated[int, DType(pl.UInt32())]
    scheduled_arrival: Annotated[int, DType(pl.UInt32())]
    actual_departure: Annotated[int | None, DType(pl.UInt32())]
    actual_arrival: Annotated[int | None, DType(pl.UInt32())]


class _FlightInfoRecord(TypedDict):
    timestamp_ms: Annotated[int, DType(pl.UInt64())]
    flightid: Annotated[int, DType(pl.UInt32())]
    latitude: Annotated[float, DType(pl.Float32())]
    longitude: Annotated[float, DType(pl.Float32())]
    track: Annotated[int | None, DType(pl.UInt16())]
    altitude: Annotated[int, DType(pl.Int32())]
    ground_speed: Annotated[int, DType(pl.Int16())]
    vertical_speed: Annotated[int | None, DType(pl.Int16())]
    on_ground: Annotated[bool, DType(pl.Boolean())]
    callsign: Annotated[str, DType(pl.String())]
    squawk: Annotated[int, DType(pl.UInt16())]
    ems: Annotated[None | EMSRecord, DType(pl.Struct(ems_struct_schema))]


class _FlightTrailRecord(TypedDict):
    flight_trail_list: Annotated[
        None | list[TrailPointRecord],
        DType(pl.List(pl.Struct(trail_point_schema))),
    ]


class FlightDetailsRecord(
    TypedDict,
    _AircraftRecord,
    _ScheduleRecord,
    _FlightProgressRecord,
    _FlightInfoRecord,
    _FlightTrailRecord,
):
    pass


flight_details_schema = to_schema(FlightDetailsRecord)


class PlaybackFlightRecord(
    TypedDict,
    _AircraftRecord,
    _ScheduleRecord,
    _FlightInfoRecord,
    _FlightTrailRecord,
):
    pass


playback_flight_schema = to_schema(PlaybackFlightRecord)
