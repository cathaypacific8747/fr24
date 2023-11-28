import sys
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    TypedDict,
    TypeVar,
    Union,
)


class Live(TypedDict):
    lat: float
    lon: float
    schd_from: str
    schd_to: str
    ac_type: str
    route: str
    logo: str
    reg: str
    callsign: str
    flight: str
    operator: str


class Airport(TypedDict):
    lat: float
    lon: float
    size: float


class Operator(TypedDict):
    operator_id: int
    iata: str
    logo: str


class Schedule(TypedDict):
    logo: str
    callsign: str
    flight: str
    operator: str


class Aircraft(TypedDict):
    equip: str
    hex: str


T = TypeVar("T", Airport, Operator, Live, Schedule, Aircraft)


if sys.version_info >= (3, 11) or TYPE_CHECKING:

    class Entry(Generic[T], TypedDict):
        id: str
        label: str
        detail: T
        type: Literal["airport", "operator", "live", "schedule", "aircraft"]
        match: Literal["icao", "iata", "begins"]
        name: str

else:

    class Entry(TypedDict):
        id: str
        label: str
        detail: dict[str, Any]
        type: Literal["airport", "operator", "live", "schedule", "aircraft"]
        match: Literal["icao", "iata", "begins"]
        name: str


class StatsEntry(TypedDict):
    all: int
    airport: int
    operator: int
    live: int
    schedule: int
    aircraft: int


class Stats(TypedDict):
    total: StatsEntry
    count: StatsEntry


class FindResult(TypedDict):
    results: list[
        Union[
            Entry[Airport],
            Entry[Operator],
            Entry[Live],
            Entry[Schedule],
            Entry[Aircraft],
        ]
    ]
    stats: Stats
