from __future__ import annotations

import polars as pl
from typing_extensions import TypedDict

# NOTE: Parquet does not support timestamp in seconds:
# https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#timestamp
# using u32 or timestamp_ms for now
flight_list_schema = {
    "flight_id": pl.UInt64(),
    "number": pl.String(),
    "callsign": pl.String(),
    "icao24": pl.UInt32(),
    "registration": pl.String(),
    "typecode": pl.String(),
    "origin": pl.String(),
    "destination": pl.String(),
    "status": pl.String(),
    "STOD": pl.Datetime("ms", time_zone="UTC"),
    "ETOD": pl.Datetime("ms", time_zone="UTC"),
    "ATOD": pl.Datetime("ms", time_zone="UTC"),
    "STOA": pl.Datetime("ms", time_zone="UTC"),
    "ETOA": pl.Datetime("ms", time_zone="UTC"),
    "ATOA": pl.Datetime("ms", time_zone="UTC"),
}


class FlightListRecord(TypedDict):
    flight_id: int | None
    number: str | None
    callsign: str | None
    icao24: int | None
    registration: str | None
    typecode: str
    origin: str | None
    destination: str | None
    status: str | None
    STOD: int | None
    ETOD: int | None
    ATOD: int | None
    STOA: int | None
    ETOA: int | None
    ATOA: int | None


playback_track_ems_struct = pl.Struct(
    {
        "timestamp": pl.UInt32(),
        "ias": pl.Int16(),
        "tas": pl.Int16(),
        "mach": pl.Int16(),
        "mcp": pl.Int32(),
        "fms": pl.Int32(),
        "autopilot": pl.Int8(),
        "oat": pl.Int8(),
        "track": pl.Float32(),
        "roll": pl.Float32(),
        "qnh": pl.UInt16(),
        "wind_dir": pl.Int16(),
        "wind_speed": pl.Int16(),
        "precision": pl.UInt8(),
        "altitude_gps": pl.Int32(),
        "emergency": pl.UInt8(),
        "tcas_acas": pl.UInt8(),
        "heading": pl.UInt16(),
    }
)


class PlaybackTrackEMSRecord(TypedDict):
    timestamp: int
    ias: int | None
    tas: int | None
    mach: float | None
    mcp: int | None
    fms: int | None
    autopilot: int | None
    oat: int | None
    track: float | None
    roll: float | None
    qnh: int | None
    wind_dir: int | None
    wind_speed: int | None
    precision: int | None
    altitude_gps: int | None
    emergency: int | None
    tcas_acas: int | None
    heading: int | None


playback_track_schema = {
    "timestamp": pl.UInt32(),
    "latitude": pl.Float32(),
    "longitude": pl.Float32(),
    "altitude": pl.Int32(),
    "ground_speed": pl.Int16(),
    "vertical_speed": pl.Int16(),
    "track": pl.Int16(),
    "squawk": pl.UInt16(),
    "ems": playback_track_ems_struct,
}


class PlaybackTrackRecord(TypedDict):
    timestamp: int
    latitude: float
    longitude: float
    altitude: int
    ground_speed: int
    vertical_speed: int | None
    track: int
    squawk: int
    ems: None | PlaybackTrackEMSRecord


live_feed_schema = {
    "timestamp": pl.UInt32(),
    "flightid": pl.UInt32(),
    "latitude": pl.Float32(),
    "longitude": pl.Float32(),
    "track": pl.UInt16(),
    "altitude": pl.Int32(),
    "ground_speed": pl.Int16(),
    "on_ground": pl.Boolean(),
    "callsign": pl.String(),
    "source": pl.UInt8(),
    "registration": pl.String(),
    "origin": pl.String(),
    "destination": pl.String(),
    "typecode": pl.String(),
    "eta": pl.UInt32(),
    "vertical_speed": pl.Int16(),  # 64 * 9-bit + 1-bit sign
    "squawk": pl.UInt16(),
    "position_buffer": pl.List(
        pl.Struct(
            {
                "delta_lat": pl.Int32(),
                "delta_lon": pl.Int32(),
                "delta_ms": pl.UInt32(),
            }
        )
    ),
}


class RecentPositionRecord(TypedDict):
    delta_lat: int
    delta_lon: int
    delta_ms: int


class FlightRecord(TypedDict):
    timestamp: int
    flightid: int
    latitude: float
    longitude: float
    track: int
    altitude: int
    ground_speed: int
    vertical_speed: int
    on_ground: bool
    callsign: str
    source: int
    registration: str
    origin: str
    destination: str
    typecode: str
    eta: int
    squawk: int
    position_buffer: list[RecentPositionRecord]


nearest_flights_schema = {
    **live_feed_schema,
    "distance": pl.UInt32(),
}


class NearbyFlightRecord(FlightRecord):
    distance: int


live_flights_status_schema = {
    "flight_id": pl.UInt32(),
    "latitude": pl.Float32(),
    "longitude": pl.Float32(),
    "status": pl.UInt8(),
    "squawk": pl.UInt16(),
}


class LiveFlightStatusRecord(TypedDict):
    flight_id: int
    latitude: float
    longitude: float
    status: int
    squawk: int


top_flights_schema = {
    "flight_id": pl.UInt32(),
    "live_clicks": pl.UInt32(),
    "total_clicks": pl.UInt32(),
    "flight_number": pl.String(),
    "callsign": pl.String(),
    "squawk": pl.UInt32(),
    "from_iata": pl.String(),
    "from_city": pl.String(),
    "to_iata": pl.String(),
    "to_city": pl.String(),
    "type": pl.String(),
    "full_description": pl.String(),
}


class TopFlightRecord(TypedDict):
    flight_id: int
    live_clicks: int
    total_clicks: int
    flight_number: str
    callsign: str
    squawk: int
    from_iata: str
    from_city: str
    to_iata: str
    to_city: str
    type: str
    full_description: str


ems_struct = pl.Struct(
    {
        "ias": pl.Int16(),
        "tas": pl.Int16(),
        "mach": pl.Int16(),
        "mcp": pl.Int32(),
        "fms": pl.Int32(),
        "oat": pl.Int8(),
        "qnh": pl.UInt16(),
        "wind_dir": pl.Int16(),
        "wind_speed": pl.Int16(),
        "altitude_gps": pl.Int32(),
        "agpsdiff": pl.Int32(),
        "apflags": pl.Int32(),
        "rs": pl.Int32(),
    }
)


class EMSRecord(TypedDict):
    ias: int | None
    tas: int | None
    mach: int | None
    mcp: int | None
    fms: int | None
    oat: int | None
    qnh: int | None
    wind_dir: int | None
    wind_speed: int | None
    altitude_gps: int | None
    agpsdiff: int | None
    apflags: int | None
    rs: int | None


flight_trail_struct = pl.Struct(
    {
        "timestamp": pl.UInt32(),
        "latitude": pl.Float32(),
        "longitude": pl.Float32(),
        "altitude": pl.Int32(),
        "ground_speed": pl.Int16(),
        "track": pl.UInt16(),
        "vertical_speed": pl.Int16(),
    }
)


class TrailPointRecord(TypedDict):
    timestamp: int
    latitude: float
    longitude: float
    altitude: int | None
    ground_speed: int | None
    track: int | None
    vertical_speed: int | None


flight_details_schema = {
    "icao_address": pl.UInt32(),
    "reg": pl.String(),
    "typecode": pl.String(),
    "flight_number": pl.String(),
    "origin_id": pl.UInt32(),
    "destination_id": pl.UInt32(),
    "diverted_id": pl.UInt32(),
    "scheduled_departure": pl.UInt32(),
    "scheduled_arrival": pl.UInt32(),
    "actual_departure": pl.UInt32(),
    "actual_arrival": pl.UInt32(),
    "traversed_distance": pl.UInt32(),
    "remaining_distance": pl.UInt32(),
    "elapsed_time": pl.UInt32(),
    "remaining_time": pl.UInt32(),
    "eta": pl.UInt32(),
    "great_circle_distance": pl.UInt32(),
    "mean_flight_time": pl.UInt32(),
    "timestamp_ms": pl.UInt64(),
    "flightid": pl.UInt32(),
    "latitude": pl.Float32(),
    "longitude": pl.Float32(),
    "track": pl.UInt16(),
    "altitude": pl.Int32(),
    "ground_speed": pl.Int16(),
    "vertical_speed": pl.Int16(),
    "on_ground": pl.Boolean(),
    "callsign": pl.String(),
    "squawk": pl.UInt16(),
    "ems": ems_struct,
    "flight_trail_list": pl.List(flight_trail_struct),
}


class FlightDetailsRecord(TypedDict):
    # aircraft
    icao_address: int
    reg: str
    typecode: str
    # schedule
    flight_number: str
    origin_id: int
    destination_id: int
    diverted_id: int
    scheduled_departure: int
    scheduled_arrival: int
    actual_departure: int | None
    actual_arrival: int | None
    # schedule
    traversed_distance: int
    remaining_distance: int
    elapsed_time: int | None
    remaining_time: int | None
    eta: int
    great_circle_distance: int
    mean_flight_time: int
    # flight info
    timestamp_ms: int
    flightid: int
    latitude: float
    longitude: float
    track: int | None
    altitude: int
    ground_speed: int
    vertical_speed: int | None
    on_ground: bool
    callsign: str
    squawk: int
    ems: None | EMSRecord
    # flight trail (available if verbose)
    flight_trail_list: None | list[TrailPointRecord]
