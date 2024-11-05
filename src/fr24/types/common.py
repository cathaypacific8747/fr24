from __future__ import annotations

from typing_extensions import NotRequired, TypedDict


class APIResult(TypedDict):
    copyright: str
    legalNotice: str


class FlightNumber(TypedDict):
    default: str | None
    alternative: NotRequired[str | None]


class AircraftModel(TypedDict):
    code: str
    text: None | str


class AircraftAge(TypedDict):
    availability: bool
    date: NotRequired[str]  # if unauthenticated


class AircraftAvailability(TypedDict):
    serialNo: bool
    age: bool


###


class _GenericStatus(TypedDict):
    text: str | None
    type: str
    color: str | None
    diverted: None


class _GenericEventTime(TypedDict):
    utc: int | None
    local: int | None


class _StatusGeneric(TypedDict):
    status: _GenericStatus
    eventTime: _GenericEventTime


class StatusData(TypedDict):
    live: bool | None
    text: str | None
    icon: str | None
    estimated: None
    ambiguous: bool
    generic: _StatusGeneric


class _Iata_Icao(TypedDict):
    iata: str | None
    icao: str


class OwnerData(TypedDict):
    name: str
    code: _Iata_Icao


class AirlineData(TypedDict):
    name: str
    code: _Iata_Icao
    short: str


###


class _AirportCode(TypedDict):
    iata: str
    icao: str


class _Country(TypedDict):
    name: str
    code: str
    id: int


class _Region(TypedDict):
    city: str


class _AirportPosition(TypedDict):
    latitude: float
    longitude: float
    country: _Country
    region: _Region


class _Timezone(TypedDict):
    name: str
    offset: int
    abbr: str
    abbrName: str | None
    isDst: bool


class Airport(TypedDict):
    name: str
    code: _AirportCode
    position: _AirportPosition
    timezone: _Timezone
    visible: NotRequired[bool]


# O/D can be null when route status is "unknown"
class AirportPairData(TypedDict):
    origin: None | Airport
    destination: None | Airport
    real: None | str


### playback and flight list


class _Image(TypedDict):
    src: str
    link: str
    copyright: str
    source: str


class ImageCollection(TypedDict):
    large: list[_Image]
    medium: list[_Image]
    thumbnails: list[_Image]
