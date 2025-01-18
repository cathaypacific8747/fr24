from __future__ import annotations

from typing import Literal

from typing_extensions import NotRequired, Required, TypedDict

from .common import (
    AircraftAge,
    AircraftAvailability,
    AircraftModel,
    AirlineData,
    AirportPairData,
    APIResult,
    FlightNumber,
    ImageCollection,
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
    olderThenFlightId: None
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


class AircraftInfo(TypedDict):
    model: AircraftModel
    registration: None | str
    owner: NotRequired[OwnerData]
    airline: NotRequired[AirlineData]
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
    aircraft: AircraftInfo
    owner: OwnerData
    airline: AirlineData
    airport: AirportPairData
    time: FlightListTime


class AircraftImage(TypedDict):
    registration: str
    images: ImageCollection


class FlightListResponse(TypedDict):
    item: Item
    page: Page
    timestamp: int
    data: list[FlightListItem] | None
    # TODO: depending on whether the flight list was queried by reg or flight
    # this may change - check this again
    aircraftInfo: AircraftInfo
    aircraftImages: list[AircraftImage]


class FlightListResult(TypedDict):
    request: FlightListRequest
    response: FlightListResponse


class FlightList(TypedDict):
    result: FlightListResult
    _api: APIResult


FLIGHT_LIST_EMPTY: FlightList = {
    "result": {
        "request": {
            "fetchBy": "flight",
            "format": "json",
            "limit": 0,
            "page": 0,
            "query": "",
            "timestamp": 0,
        },
        "response": {
            "item": {"current": 0, "total": None, "limit": 0},
            "page": {"current": 0, "more": False, "total": None},
            "timestamp": 0,
            "data": None,
            "aircraftInfo": {
                "model": {"code": "", "text": ""},
                "registration": None,
                "country": None,
                "hex": None,
                "restricted": False,
                "serialNo": None,
                "age": {"availability": False},
                "availability": {"serialNo": False, "age": False},
            },
            "aircraftImages": [],
        },
    },
    "_api": {"copyright": "", "legalNotice": ""},
}
"""An object with no flight list data, for use as a default value."""
