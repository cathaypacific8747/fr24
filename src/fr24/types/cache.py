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


playback_track_schema = {
    "timestamp": pl.UInt32(),
    "latitude": pl.Float32(),
    "longitude": pl.Float32(),
    "altitude": pl.Int32(),
    "ground_speed": pl.Int16(),
    "vertical_speed": pl.Int16(),
    "track": pl.Int16(),
    "squawk": pl.UInt16(),
    "ems": pl.Struct(
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
    ),
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
