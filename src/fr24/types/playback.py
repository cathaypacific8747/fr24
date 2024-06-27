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
    OwnerData,
    StatusData,
)


class PlaybackRequest(TypedDict, total=False):
    callback: None
    device: None | str
    flightId: Required[str]
    format: Literal["json"]
    pk: None
    timestamp: int | None
    token: None | str


class FlightIdentification(TypedDict):
    id: str | int
    number: FlightNumber
    callsign: str


class AircraftIdentification(TypedDict):
    modes: str
    registration: str
    serialNo: None | str
    age: NotRequired[AircraftAge]  # if unauthenticated
    availability: NotRequired[AircraftAvailability]  # if unauthenticated


class AircraftData(TypedDict):
    model: AircraftModel
    identification: AircraftIdentification
    availability: AircraftAvailability


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
    fpm: int | None
    ms: int | None


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
    """
    !!! warning
        The JSON response claims that `heading` is available, but ADS-B only
        transmits the [ground track](https://mode-s.org/decode/content/ads-b/4-surface-position.html#ground-track).
        [Heading](https://mode-s.org/decode/content/mode-s/7-ehs.html#heading-and-speed-report-bds-60)
        is only available in [EMS][fr24.types.playback.EMS] data.

        This field is renamed to `track` to avoid confusion in
        [fr24.history.playback_track_dict][].
    """
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
