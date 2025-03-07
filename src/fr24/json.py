from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Generic, TypeVar, cast

import httpx
import polars as pl

from .types.airport_list import AirportList
from .types.cache import flight_list_schema, playback_track_schema
from .types.find import Find
from .types.flight_list import FlightList
from .types.playback import Playback
from .utils import DEFAULT_HEADERS, to_unix_timestamp

if TYPE_CHECKING:
    from typing import Annotated, Any, Literal

    from .types.airport_list import AirportRequest
    from .types.authentication import Authentication
    from .types.cache import (
        FlightListRecord,
        PlaybackTrackEMSRecord,
        PlaybackTrackRecord,
    )
    from .types.flight_list import FlightListItem, FlightListRequest
    from .types.playback import (
        FlightData,
        PlaybackRequest,
        TrackData,
    )

_log = logging.getLogger(__name__)

# NOTE: we intentionally use dataclass to store request data so we can
# serialise it to disk easily.


@dataclass
class FlightListParams:
    """
    Parameters to fetch metadata/history of flights for
    *either* a given aircraft registration or flight number.
    """

    # NOTE: consider moving away from internally tagged enum
    reg: str | None = None
    """Aircraft registration (e.g. `B-HUJ`)"""
    flight: str | None = None
    """Flight number (e.g. `CX8747`)"""
    page: int = 1
    """Page number"""
    limit: int = 10
    """Number of results per page - use `100` if authenticated."""
    timestamp: int | datetime | str | Literal["now"] | None = "now"
    """Show flights with ATD before this Unix timestamp"""

    def __post_init__(self) -> None:
        if self.reg is None and self.flight is None:
            raise ValueError(
                "expected one of `reg` or `flight` to be set, "
                "but both are `None`"
            )
        if self.reg is not None and self.flight is not None:
            raise ValueError(
                "expected only one of `reg` or `flight` to be set, "
                "but both are not `None`"
            )

    @property
    def kind(self) -> Literal["reg", "flight"]:
        return "reg" if self.reg is not None else "flight"

    @property
    def ident(self) -> str:
        return self.reg if self.reg is not None else self.flight  # type: ignore


async def flight_list(
    client: httpx.AsyncClient,
    params: FlightListParams,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, FlightList]:
    """
    Query flight list data.

    To determine if there are more pages to query, check the response
    [.result.response.page.more][fr24.types.flight_list.Page.more].

    Includes basic information such as status, O/D, scheduled/estimated/real
    times: see [fr24.types.flight_list.FlightList][] for more details.

    :param client: HTTPX async client
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(params.timestamp)

    key, value = params.kind, params.ident

    # TODO: remove duplication
    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device
    request_data: FlightListRequest = {
        "query": value,
        "fetchBy": key,
        "page": params.page,
        "limit": params.limit,
    }

    if timestamp is not None:
        request_data["timestamp"] = timestamp

    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        request_data["token"] = auth["userData"]["subscriptionKey"]
    else:
        request_data["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/flight/list.json",
        headers=headers,
        params=request_data,  # type: ignore
    )

    response = await client.send(request)
    return response


@dataclass
class AirportListParams:
    """
    Request data to fetch metadata/history of flights
    """

    airport: str
    """IATA airport code (e.g. `HKG`)"""
    mode: Literal["arrivals"] | Literal["departures"] | Literal["ground"]
    """arrivals, departures or on ground aircraft"""
    page: int = 1
    """Page number"""
    limit: int = 10
    """Number of results per page - use `100` if authenticated."""
    timestamp: int | datetime | str | None = "now"
    """Show flights with STA before this timestamp"""


async def airport_list(
    client: httpx.AsyncClient,
    params: AirportListParams,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, AirportList]:
    """
    Fetch aircraft arriving, departing or on ground at a given airport.

    Returns on ground/scheduled/estimated/real times: see
    [fr24.types.flight_list.FlightListItem][] for more details.

    :param client: HTTPX async client
    :param auth: Authentication data
    :returns: the raw binary response, representing a JSON-encoded
        [fr24.types.flight_list.FlightList][].
    """
    timestamp = to_unix_timestamp(params.timestamp)

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device

    request_data: AirportRequest = {
        "code": params.airport,
        "plugin[]": ["schedule"],
        "plugin-setting[schedule][mode]": params.mode,
        "page": params.page,
        "limit": params.limit,
    }

    if timestamp is not None:
        request_data["plugin-setting[schedule][timestamp]"] = timestamp

    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        request_data["token"] = auth["userData"]["subscriptionKey"]
    else:
        request_data["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/airport.json",
        headers=headers,
        params=request_data,  # type: ignore
    )

    response = await client.send(request)
    return response


@dataclass
class PlaybackParams:
    """
    Request data to fetch historical track playback data for a given flight.
    """

    flight_id: int | str
    """fr24 flight id, represented in hex"""
    timestamp: int | str | datetime | None = None
    """
    Unix timestamp (seconds) of ATD - optional, but it is recommended to
    include it
    """


async def playback(
    client: httpx.AsyncClient,
    params: PlaybackParams,
    auth: None | Authentication = None,
) -> Annotated[httpx.Response, Playback]:
    """
    Fetch historical track playback data for a given flight.

    :param client: HTTPX async client
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(params.timestamp)
    flight_id = (
        f"{params.flight_id:x}"
        if not isinstance(params.flight_id, str)
        else params.flight_id
    )  # TODO: move this up

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device
    request_data: PlaybackRequest = {
        "flightId": flight_id,
    }
    if timestamp is not None:
        request_data["timestamp"] = timestamp
    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        request_data["token"] = auth["userData"]["subscriptionKey"]
    else:
        request_data["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/flight-playback.json",
        headers=headers,
        params=request_data,  # type: ignore
    )

    response = await client.send(request)
    return response


# NOTE: not using dataclasses for now.


async def find(
    client: httpx.AsyncClient, query: str
) -> Annotated[httpx.Response, Find]:
    """
    General search.

    :param query: Airport, schedule (HKG-CDG), or aircraft.
    """
    request = httpx.Request(
        "GET",
        url="https://www.flightradar24.com/v1/search/web/find",
        params={"query": query, "limit": 50},
    )
    response = await client.send(request)
    return response


#
# helpers
#

# workaround for py<3.12: https://docs.python.org/3/reference/compound_stmts.html#type-params
# just to silence mypy
_TypedDictT = TypeVar("_TypedDictT")


class _Parser(Generic[_TypedDictT]):
    @staticmethod
    def parse_json(
        response: Annotated[httpx.Response, _TypedDictT],
    ) -> _TypedDictT:
        """
        Parses binary representation into a python object (typed dict).

        :raises httpx.HTTPStatusError: if the response did not succeed
        """
        import orjson

        response.raise_for_status()
        return cast(_TypedDictT, orjson.loads(response.content))


flight_list_parse = _Parser[FlightList].parse_json
airport_list_parse = _Parser[AirportList].parse_json
playback_parse = _Parser[Playback].parse_json
find_parse = _Parser[Find].parse_json


def playback_metadata_dict(flight: FlightData) -> dict[str, Any]:
    """
    Flatten and rename important variables in the flight metadata to a
    dictionary.
    """
    ident = flight["identification"]
    sta = flight["status"]["generic"]
    owner = flight["owner"]
    aircraft = flight["aircraft"]
    airline = flight["airline"]
    origin = flight["airport"]["origin"]
    dest = flight["airport"]["destination"]
    return {
        "flight_id": int(id_, 16)
        if isinstance(id_ := ident["id"], str)
        else id_,
        "callsign": ident["callsign"],
        "flight_number": ident["number"].get("default", None),
        "status_type": sta["status"]["type"],
        "status_text": sta["status"]["text"],
        "status_diverted": sta["status"]["diverted"],
        "status_time": int(time)
        if (time := sta["eventTime"]["utc"]) is not None
        else None,
        "model_code": aircraft["model"]["code"]
        if aircraft is not None
        else None,
        "icao24": int(aircraft["identification"]["modes"], 16)
        if aircraft is not None
        else None,
        "registration": aircraft["identification"]["registration"]
        if aircraft is not None
        else None,
        "owner": owner["code"]["icao"] if owner is not None else None,
        "airline": airline["code"]["icao"] if airline is not None else None,
        "origin": origin["code"]["icao"] if origin is not None else None,
        "destination": dest["code"]["icao"] if dest is not None else None,
        "median_delay": delay_med
        if (delay_med := flight["median"]["delay"]) is not None
        else None,
        "median_time": int(time_med)
        if (time_med := flight["median"]["timestamp"]) is not None
        else None,
    }


def playback_track_dict(point: TrackData) -> PlaybackTrackRecord:
    """
    Flatten and rename each variable in this observation into a new dictionary.

    !!! note
        The JSON response claims that `heading` is available, but ADS-B only
        transmits the [ground track](https://mode-s.org/decode/content/ads-b/4-surface-position.html#ground-track).
        [Heading](https://mode-s.org/decode/content/mode-s/7-ehs.html#heading-and-speed-report-bds-60)
        is only available in [EMS][fr24.types.playback.EMS] data.

        We rename it to `track` to avoid confusion.
    """
    return {
        "timestamp": point["timestamp"],
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "altitude": point["altitude"]["feet"],
        "ground_speed": point["speed"]["kts"],
        "vertical_speed": point["verticalSpeed"]["fpm"],
        "track": point["heading"],
        "squawk": int(point["squawk"], base=8),
    }


def playback_track_ems_dict(point: TrackData) -> PlaybackTrackEMSRecord | None:
    """
    If the Enhanced Mode-S data is available in this observation,
    flatten and rename each variable to a dictionary. Otherwise, return `None`.
    """
    if e := point["ems"]:
        return {
            "timestamp": e["ts"],
            "ias": e["ias"],
            "tas": e["tas"],
            "mach": e["mach"],
            "mcp": e["mcp"],
            "fms": e["fms"],
            "autopilot": e["autopilot"],
            "oat": e["oat"],
            "track": e["trueTrack"],
            "roll": e["rollAngle"],
            "qnh": e["qnh"],
            "wind_dir": e["windDir"],
            "wind_speed": e["windSpd"],
            "precision": e["precision"],
            "altitude_gps": e["altGPS"],
            "emergency": e["emergencyStatus"],
            "tcas_acas": e["tcasAcasDtatus"],
            "heading": e["heading"],
        }
    return None


def playback_df(data: Playback) -> pl.DataFrame:
    """
    Parse each [fr24.types.playback.TrackData][] in the API response into a
    dataframe.

    If the response is empty, a warning is logged and an empty table is returned
    """
    flight = data["result"]["response"]["data"]["flight"]
    if len(track := flight["track"]) == 0:
        _log.warning("no data in response, table will be empty")
    return pl.DataFrame(
        [
            {
                **playback_track_dict(point),
                "ems": playback_track_ems_dict(point),
            }
            for point in track
        ],
        schema=playback_track_schema,
    )
    # NOTE: original implementation returns pl.DateTime instead of timestamp


def flight_list_dict(entry: FlightListItem) -> FlightListRecord:
    """
    Flatten a flight entry into dict, converting fr24 hex ids into integers.
    """
    orig = entry["airport"]["origin"]
    dest = entry["airport"]["destination"]
    icao24 = entry["aircraft"]["hex"]
    id_ = entry["identification"]["id"]
    stod = entry["time"]["scheduled"]["departure"]
    etod = entry["time"]["estimated"]["departure"]
    atod = entry["time"]["real"]["departure"]
    stoa = entry["time"]["scheduled"]["arrival"]
    etoa = entry["time"]["estimated"]["arrival"]
    atoa = entry["time"]["real"]["arrival"]
    return {
        "flight_id": int(id_, 16) if id_ is not None else None,
        "number": entry["identification"]["number"]["default"],
        "callsign": entry["identification"]["callsign"],
        "icao24": int(icao24, 16) if icao24 is not None else None,
        "registration": entry["aircraft"]["registration"],
        "typecode": entry["aircraft"]["model"]["code"],
        "origin": orig["code"]["icao"] if orig is not None else None,
        "destination": dest["code"]["icao"] if dest is not None else None,
        "status": entry["status"]["text"],
        "STOD": stod * 1000 if stod is not None else None,
        "ETOD": etod * 1000 if etod is not None else None,
        "ATOD": atod * 1000 if atod is not None else None,
        "STOA": stoa * 1000 if stoa is not None else None,
        "ETOA": etoa * 1000 if etoa is not None else None,
        "ATOA": atoa * 1000 if atoa is not None else None,
    }


def flight_list_df(data: FlightList) -> pl.DataFrame:
    """
    Parse each [fr24.types.flight_list.FlightListItem][] in the API response
    into a polars dataframe.

    If the response is empty, a warning is logged and an empty table is returned
    """
    if (flights := data["result"]["response"]["data"]) is None:
        _log.warning("no data in response, table will be empty")
        return pl.DataFrame(schema=flight_list_schema)
    return pl.DataFrame(
        [flight_list_dict(f) for f in flights],
        schema=flight_list_schema,
    )
