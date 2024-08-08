from __future__ import annotations

from typing import Literal, Optional

from typing_extensions import TypedDict

from .common import APIResult
from .flight_list import FlightListResponse


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
