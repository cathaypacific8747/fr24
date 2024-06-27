from __future__ import annotations

from typing import Literal

from typing_extensions import Required, TypedDict

from .common import (
    AircraftAge,
    AircraftAvailability,
    AircraftModel,
    AirlineData,
    AirportPairData,
    APIResult,
    FlightNumber,
    OwnerData,
    StatusData,
)


class FlightListRequest(TypedDict, total=False):
    callback: None
    device: None | str
    fetchBy: Required[str]
    filterBy: str | None
    format: Literal["json"]
    limit: Required[int]
    olderThenFlightID: None
    page: int
    pk: None
    query: Required[str]
    timestamp: int
    token: None | str


class Item(TypedDict):
    current: int
    total: None | int
    limit: int


class Page(TypedDict):
    current: int
    more: bool
    total: None | int


class Identification(TypedDict):
    id: str | None
    """icao hex"""
    row: int
    """internal row id"""
    number: FlightNumber
    callsign: str | None
    codeshare: None


class FlightListCountry(TypedDict):
    id: int | None
    name: str | None
    alpha2: str | None
    alpha3: str | None


class FlightListAircraftData(TypedDict):
    model: AircraftModel
    registration: None | str
    country: None | FlightListCountry
    hex: None | str
    restricted: bool
    serialNo: None | str
    age: AircraftAge
    availability: AircraftAvailability


class Interval(TypedDict):
    departure: None | int
    arrival: None | int


class TimeOther(TypedDict):
    eta: None | int
    updated: None | int
    duration: None | int


class FlightListTime(TypedDict):
    scheduled: Interval
    real: Interval
    estimated: Interval
    other: TimeOther


class FlightListItem(TypedDict):
    identification: Identification
    status: StatusData
    aircraft: FlightListAircraftData
    owner: OwnerData
    airline: AirlineData
    airport: AirportPairData
    time: FlightListTime


class FlightListResponse(TypedDict):
    item: Item
    page: Page
    timestamp: int
    data: None | list[FlightListItem]


class FlightListResult(TypedDict):
    request: FlightListRequest
    response: FlightListResponse


class FlightList(TypedDict):
    result: FlightListResult
    _api: APIResult
