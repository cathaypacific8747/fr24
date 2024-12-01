from __future__ import annotations

import pyarrow as pa
from typing_extensions import TypedDict

# NOTE: Parquet does not support timestamp in seconds:
# https://github.com/apache/parquet-format/blob/master/LogicalTypes.md#timestamp
# using u32 or pa.timestamp("ms") for now
flight_list_schema = pa.schema(
    [
        pa.field("flight_id", pa.uint64()),
        pa.field("number", pa.string()),
        pa.field("callsign", pa.string()),
        pa.field("icao24", pa.uint32()),
        pa.field("registration", pa.string()),
        pa.field("typecode", pa.string()),
        pa.field("origin", pa.string()),
        pa.field("destination", pa.string()),
        pa.field("status", pa.string()),
        pa.field("STOD", pa.timestamp("ms", tz="UTC")),
        pa.field("ETOD", pa.timestamp("ms", tz="UTC")),
        pa.field("ATOD", pa.timestamp("ms", tz="UTC")),
        pa.field("STOA", pa.timestamp("ms", tz="UTC")),
        pa.field("ETOA", pa.timestamp("ms", tz="UTC")),
        pa.field("ATOA", pa.timestamp("ms", tz="UTC")),
    ]
)


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


playback_track_schema = pa.schema(
    [
        pa.field("timestamp", pa.uint32()),
        pa.field("latitude", pa.float32()),
        pa.field("longitude", pa.float32()),
        pa.field("altitude", pa.int32()),
        pa.field("ground_speed", pa.int16()),
        pa.field("vertical_speed", pa.int16()),
        pa.field("track", pa.int16()),
        pa.field("squawk", pa.uint16()),
        pa.field(
            "ems",
            pa.struct(
                [
                    pa.field("timestamp", pa.uint32()),
                    pa.field("ias", pa.int16()),
                    pa.field("tas", pa.int16()),
                    pa.field("mach", pa.int16()),
                    pa.field("mcp", pa.int32()),
                    pa.field("fms", pa.int32()),
                    pa.field("autopilot", pa.int8()),
                    pa.field("oat", pa.int8()),
                    pa.field("track", pa.float32()),
                    pa.field("roll", pa.float32()),
                    pa.field("qnh", pa.uint16()),
                    pa.field("wind_dir", pa.int16()),
                    pa.field("wind_speed", pa.int16()),
                    pa.field("precision", pa.uint8()),
                    pa.field("altitude_gps", pa.int32()),
                    pa.field("emergency", pa.uint8()),
                    pa.field("tcas_acas", pa.uint8()),
                    pa.field("heading", pa.uint16()),
                ]
            ),
        ),
    ],
)


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


# NOTE: not using pa.timestamp() to save space
live_feed_schema = pa.schema(
    [
        pa.field("timestamp", pa.uint32()),
        pa.field("flightid", pa.uint32()),
        pa.field("latitude", pa.float32()),
        pa.field("longitude", pa.float32()),
        pa.field("track", pa.uint16()),
        pa.field("altitude", pa.int32()),
        pa.field("ground_speed", pa.int16()),
        pa.field("on_ground", pa.bool_()),
        pa.field("callsign", pa.string()),
        pa.field("source", pa.uint8()),
        pa.field("registration", pa.string()),
        pa.field("origin", pa.string()),
        pa.field("destination", pa.string()),
        pa.field("typecode", pa.string()),
        pa.field("eta", pa.uint32()),
        pa.field("vertical_speed", pa.int16()),  # 64 * 9-bit + 1-bit sign
        pa.field("squawk", pa.uint16()),
        pa.field(
            "position_buffer",
            pa.list_(
                pa.struct(
                    [
                        pa.field("delta_lat", pa.int32()),
                        pa.field("delta_lon", pa.int32()),
                        pa.field("delta_ms", pa.uint32()),
                    ]
                )
            ),
        ),
    ]
)


class RecentPosition(TypedDict):
    delta_lat: int
    delta_lon: int
    delta_ms: int


class LiveFeedRecord(TypedDict):
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
    position_buffer: list[RecentPosition]
