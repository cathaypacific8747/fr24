from __future__ import annotations

from typing import TypedDict

import pyarrow as pa

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
        pa.field("STOD", pa.timestamp("s")),
        pa.field("ETOD", pa.timestamp("s")),
        pa.field("ATOD", pa.timestamp("s")),
        pa.field("STOA", pa.timestamp("s")),
        pa.field("ETOA", pa.timestamp("s")),
        pa.field("ATOA", pa.timestamp("s")),
    ]
)


class FlightListRecord(TypedDict):
    flight_id: int | None
    number: str
    callsign: str | None
    icao24: int | None
    registration: str | None
    typecode: str
    origin: str | None
    destination: str | None
    status: str
    STOD: int | None
    ETOD: int | None
    ATOD: int | None
    STOA: int | None
    ETOA: int | None
    ATOA: int | None


# TODO: remove pandas serialisation and force this schema
livefeed_schema = pa.schema(
    [
        pa.field("flightid", pa.uint64()),
        pa.field("latitude", pa.float32()),
        pa.field("longitude", pa.float32()),
        pa.field("heading", pa.uint16()),
        pa.field("altitude", pa.int32()),
        pa.field("ground_speed", pa.int16()),
        pa.field("timestamp", pa.uint32()),
        pa.field("on_ground", pa.bool_()),
        pa.field("callsign", pa.string()),
        pa.field("source", pa.uint8()),
        pa.field("extra_info.reg", pa.string()),
        pa.field("extra_info.route.from", pa.string()),
        pa.field("extra_info.route.to", pa.string()),
        pa.field("extra_info.type", pa.string()),
        pa.field("extra_info.schedule.eta", pa.uint32()),
    ]
)
