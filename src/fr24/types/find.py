from __future__ import annotations

from typing import Literal, Union

from typing_extensions import Annotated, NotRequired, TypedDict


class Live(TypedDict):
    lat: float
    lon: float
    schd_from: str
    schd_to: NotRequired[str]
    ac_type: str
    route: str
    logo: NotRequired[str]
    reg: str
    callsign: NotRequired[str]
    flight: NotRequired[str]
    operator: NotRequired[str]


class Airport(TypedDict):
    lat: float
    lon: float
    size: float


class Operator(TypedDict):
    operator_id: int
    iata: NotRequired[str]
    logo: NotRequired[str]


class Schedule(TypedDict):
    logo: NotRequired[str]
    callsign: NotRequired[str]
    flight: str
    operator: NotRequired[str]
    operator_id: NotRequired[int]
    schd_from: NotRequired[str]
    schd_to: NotRequired[str]


class Aircraft(TypedDict):
    owner: str  # icao
    equip: str  # aircraft type
    hex: str
    operator_id: int
    logo: str


class EntryBase(TypedDict):
    label: str
    name: NotRequired[str]


Iata = Annotated[str, "IATA"]
Icao = Annotated[str, "ICAO"]


class AirportEntry(EntryBase):
    id: Iata | Icao  # iata if match == "begins"
    detail: Airport
    type: Literal["airport"]
    match: Literal["icao", "iata", "begins", "contains"]


class OperatorEntry(EntryBase):
    id: str
    detail: Operator
    type: Literal["operator"]
    match: Literal["begins", "icao"]


class LiveEntry(EntryBase):
    id: str
    detail: Live
    type: Literal["live"]
    match: Literal["route", "begins"]


class ScheduleEntry(EntryBase):
    id: str
    detail: Schedule
    type: Literal["schedule"]
    match: Literal["route", "begins"]


class AircraftEntry(EntryBase):
    id: str
    detail: Aircraft
    type: Literal["aircraft"]
    match: Literal["begins"]


Entry = Union[
    AirportEntry, OperatorEntry, LiveEntry, ScheduleEntry, AircraftEntry
]
# NOTE: in tests, we use Annotated[Entry, pydantic.Discriminator("type")]
# not adding here because pydantic belongs to test dependencies


class StatsEntry(TypedDict):
    all: NotRequired[int]
    airport: int
    operator: int
    live: int
    schedule: int
    aircraft: int


class Stats(TypedDict):
    total: StatsEntry
    count: StatsEntry


class FindResult(TypedDict):
    results: list[Entry]
    stats: Stats
