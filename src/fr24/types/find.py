from typing import Literal

from typing_extensions import NewType, NotRequired, TypedDict


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
    id: str
    label: str
    name: NotRequired[str]


Iata = NewType("Iata", str)
Icao = NewType("Icao", str)


class AirportEntry(EntryBase):
    id: Iata | Icao  # iata if match == "begins"
    detail: Airport
    type: Literal["airport"]
    match: Literal["icao", "iata", "begins", "contains"]


class OperatorEntry(EntryBase):
    detail: Operator
    type: Literal["operator"]
    match: Literal["begins", "icao"]


class LiveEntry(EntryBase):
    detail: Live
    type: Literal["live"]
    match: Literal["route", "begins"]


class ScheduleEntry(EntryBase):
    detail: Schedule
    type: Literal["schedule"]
    match: Literal["route", "begins"]


class AircraftEntry(EntryBase):
    detail: Aircraft
    type: Literal["aircraft"]
    match: Literal["begins"]


Entry = AirportEntry | OperatorEntry | LiveEntry | ScheduleEntry | AircraftEntry
# NOTE: in tests, we use Annotated[Result, pydantic.Discriminator("type")]
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
