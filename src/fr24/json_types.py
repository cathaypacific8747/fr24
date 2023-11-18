from typing import Literal, TypedDict


class APIResult(TypedDict):
    copyright: str
    legalNotice: str


class PlaybackRequest(TypedDict):
    callback: None
    device: None | str
    flightId: str
    format: Literal["json"]
    pk: None
    timestamp: int
    token: None | str


class FlightNumber(TypedDict):
    default: str
    alternative: None


class FlightIdentification(TypedDict):
    id: str
    number: FlightNumber
    callsign: str


class EventTime:
    utc: int
    local: int


class GenericStatus(TypedDict):
    text: str
    type: str
    color: str
    diverted: None
    eventTime: EventTime


class StatusData(TypedDict):
    live: bool
    text: str
    icon: str
    estimated: None
    ambiguous: bool
    generic: GenericStatus


class AircraftModel(TypedDict):
    code: str
    text: str


class AircraftAge(TypedDict):
    availability: bool


class AircraftAvailability(TypedDict):
    serialNo: bool
    age: bool


class AircraftIdentification(TypedDict):
    modes: str
    registration: str
    serialNo: None | str
    age: AircraftAge
    availability: AircraftAvailability


class AircraftData(TypedDict):
    model: AircraftModel
    identification: AircraftIdentification
    availability: AircraftAvailability


class IATA_ICAO(TypedDict):
    iata: str
    icao: str


class OwnerData(TypedDict):
    name: str
    code: IATA_ICAO


class AirlineData(TypedDict):
    name: str
    code: IATA_ICAO
    short: str


class AirportCode(TypedDict):
    iata: str
    icao: str


class Country:
    name: str
    code: str
    id: int


class Region:
    city: str


class AirportPosition(TypedDict):
    latitude: float
    longitude: float
    country: Country
    region: Region


class Timezone(TypedDict):
    name: str
    offset: int
    abbr: str
    abbrName: str
    isDst: bool


class Airport(TypedDict):
    name: str
    code: AirportCode
    position: AirportPosition
    timezone: Timezone
    real: None


class AirportPairData(TypedDict):
    origin: Airport
    destination: Airport
    real: None | str


class Median(TypedDict):
    time: int
    delay: int
    timestamp: int


class Altitude(TypedDict):
    feet: int
    meters: int


class Speed(TypedDict):
    kmh: float
    kts: int
    mph: float


class VerticalSpeed(TypedDict):
    fpm: int
    ms: int


class TrackData(TypedDict):
    latitude: float
    longitude: float
    altitude: Altitude
    speed: Speed
    verticalSpeed: VerticalSpeed
    heading: int
    squawk: str
    timestamp: int
    ems: None  # | EMS


class Thumbnail(TypedDict):
    src: str
    link: str
    copyright: str
    source: str


class AircraftImages(TypedDict):
    thumbnails: list[Thumbnail]


class FlightData(TypedDict):
    identification: FlightIdentification
    status: StatusData
    aircraft: AircraftData
    owner: OwnerData
    airline: AirlineData
    airport: AirportPairData
    median: Median
    track: list[TrackData]
    aircraftImages: AircraftImages


class PlaybackData(TypedDict):
    flight: FlightData


class PlaybackResponse(TypedDict):
    timestamp: int
    altitudeFiltered: bool
    data: PlaybackData


class PlaybackResult(TypedDict):
    request: PlaybackRequest
    response: PlaybackResponse


class Playback(TypedDict):
    result: PlaybackResult
    _api: APIResult


class FlightListRequest(TypedDict):
    callback: None
    device: None | str
    fetchBy: str
    filterBy: str
    format: Literal["json"]
    limit: int
    olderThenFlightID: None
    page: int
    pk: None
    query: str
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
    id: None
    row: int
    number: FlightNumber
    callsign: str | None
    codeshare: None


class FlightListAircraftData(TypedDict):
    model: AircraftModel
    hex: None | str
    registration: None | str
    serialNo: None | str
    age: None | str
    restricted: None | str
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
    data: list[FlightListItem]


class FlightListResult(TypedDict):
    request: FlightListRequest
    response: FlightListResponse


class FlightList(TypedDict):
    result: FlightListResult
    _api: APIResult
