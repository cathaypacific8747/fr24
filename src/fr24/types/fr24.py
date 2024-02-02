from __future__ import annotations

from typing import Literal, Optional, TypedDict

from typing_extensions import Required


class User(TypedDict):
    id: int
    identity: str
    locale: str


class Features(TypedDict):
    ...  # useless anyway


class UserData(TypedDict, total=False):
    accessToken: None | str
    accountType: str
    countryCode: None | str
    dateExpires: int
    dateLastLogin: str
    features: Features
    hasConsented: bool
    hasPassword: bool
    idUser: int
    identity: str
    isActive: bool
    isAnonymousAccount: bool
    isLoggedIn: bool
    localeCode: str
    name: None
    oAuth: None
    oAuthType: None
    publicKey: None
    subscriptionKey: None | str
    tokenLogin: str
    typeSource: str


class Authentication(TypedDict, total=False):
    message: str
    msg: str
    response_code: int
    responseCode: int
    status: str
    success: bool
    token: str
    user: User
    features: Features
    userData: Required[UserData]


class APIResult(TypedDict):
    copyright: str
    legalNotice: str


class PlaybackRequest(TypedDict, total=False):
    callback: None
    device: None | str
    flightId: Required[str]
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


class GenericEventTime(TypedDict):
    utc: int | None
    local: int | None


class StatusGeneric(TypedDict):
    status: GenericStatus
    eventTime: GenericEventTime


class StatusData(TypedDict):
    live: bool
    text: str
    icon: str
    estimated: None
    ambiguous: bool
    generic: StatusGeneric


class AircraftModel(TypedDict):
    code: str
    text: None | str


class AircraftAge(TypedDict):
    availability: bool
    date: str


class AircraftAvailability(TypedDict):
    serialNo: bool
    age: bool


class AircraftIdentification(TypedDict):
    modes: str
    registration: str
    serialNo: None | str
    age: None | AircraftAge
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


class Country(TypedDict):
    name: str
    code: str
    id: int


class Region(TypedDict):
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


# O/D can be null when status is "unknown"
class AirportPairData(TypedDict):
    origin: None | Airport
    destination: None | Airport
    real: None | str


class Median(TypedDict):
    time: int | None
    delay: int | None
    timestamp: int | None


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


class EMS(TypedDict):
    ts: int
    ias: int | None
    tas: int | None
    mach: int | None
    mcp: int | None
    fms: int | None
    autopilot: None
    oat: int | None
    trueTrack: float | None
    rollAngle: float | None
    qnh: None
    windDir: int | None
    windSpd: int | None
    precision: int | None
    altGPS: int | None
    emergencyStatus: int | None
    tcasAcasDtatus: int | None
    heading: int | None


class TrackData(TypedDict):
    latitude: float
    longitude: float
    altitude: Altitude
    speed: Speed
    verticalSpeed: VerticalSpeed
    heading: int
    squawk: str
    timestamp: int
    ems: None | EMS


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
    aircraft: AircraftData | None
    owner: OwnerData | None
    airline: AirlineData | None
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


class FlightListRequest(TypedDict, total=False):
    callback: None
    device: None | str
    fetchBy: Required[str]
    filterBy: str
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
    data: None | list[FlightListItem]


class FlightListResult(TypedDict):
    request: FlightListRequest
    response: FlightListResponse


class FlightList(TypedDict):
    result: FlightListResult
    _api: APIResult


class Schedule(TypedDict):
    mode: Literal["departures", "arrivals"] | None
    timestamp: int


Plugin = Literal[
    "details",
    "runways",
    "schedule",
    "satelliteImage",
    "scheduledRoutesStatistics",
    "weather",
]


class PluginSetting(TypedDict, total=False):
    schedule: Schedule


AirportRequest = TypedDict(
    # We need this syntax because of the plugin-setting parameter
    "AirportRequest",
    {
        "callback": None,
        "code": str,
        "device": Optional[str],
        "fleet": Optional[str],
        "format": Literal["json"],
        "limit": int,
        "page": int,
        "pk": None,
        "plugin": list[Plugin],
        "plugin[]": list[Plugin],
        "plugin-setting": PluginSetting,
        "plugin-setting[schedule][mode]": str,
        "plugin-setting[schedule][timestamp]": int,
        "token": Optional[str],
    },
    total=False,
)


class AirportSchedule(TypedDict):
    arrivals: FlightListResponse
    departures: FlightListResponse


class AirportPluginData(TypedDict):
    schedule: AirportSchedule


class AirportListData(TypedDict):
    pluginData: AirportPluginData


class AirportResponse(TypedDict):
    airport: AirportListData


class AirportResult(TypedDict):
    request: AirportRequest
    response: AirportResponse


class AirportList(TypedDict):
    result: AirportResult
    _api: APIResult
