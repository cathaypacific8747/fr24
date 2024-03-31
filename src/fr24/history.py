from __future__ import annotations

import secrets
from datetime import datetime
from typing import Literal

import httpx

import pandas as pd

from .common import DEFAULT_HEADERS, to_unix_timestamp
from .types.cache import (
    FlightListRecord,
    PlaybackTrackEMSRecord,
    PlaybackTrackRecord,
)
from .types.fr24 import (
    AirportList,
    AirportRequest,
    Authentication,
    FlightData,
    FlightList,
    FlightListItem,
    FlightListRequest,
    Playback,
    PlaybackRequest,
    TrackData,
)


async def flight_list(
    client: httpx.AsyncClient,
    reg: None | str = None,
    flight: None | str = None,
    page: int = 1,
    limit: int = 10,
    timestamp: int | datetime | pd.Timestamp | str | None = "now",
    auth: None | Authentication = None,
) -> FlightList:
    """
    Fetch metadata/history of flights for a given aircraft or flight number.

    Includes basic information such as status, O/D, scheduled/estimated/real
    times: see [fr24.types.fr24.FlightData][] for more details.

    Use *either* `reg` or `flight` to query.
    To determine if there are more pages to query, check the response
    [.result.response.page.more][fr24.types.fr24.Page.more].

    :param client: HTTPX async client
    :param reg: Aircraft registration (e.g. `B-HUJ`)
    :param flight: Flight number (e.g. `CX8747`)
    :param page: Page number
    :param limit: Number of results per page (max 100)
    :param timestamp: Show flights with ATD before this Unix timestamp
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(timestamp)

    if reg is not None:
        key, value = "reg", reg
    elif flight is not None:
        key, value = "flight", flight
    else:
        msg = "One named arguments among `reg` and `flight` is expected"
        raise TypeError(msg)

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device
    params: FlightListRequest = {
        "query": value,
        "fetchBy": key,
        "page": page,
        "limit": limit,
    }

    if timestamp is not None:
        params["timestamp"] = timestamp

    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        params["token"] = auth["userData"]["subscriptionKey"]
    else:
        params["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/flight/list.json",
        headers=headers,
        params=params,  # type: ignore
    )

    response = await client.send(request)
    response.raise_for_status()
    return response.json()  # type: ignore


async def airport_list(
    client: httpx.AsyncClient,
    airport: str,
    mode: Literal["arrivals"] | Literal["departures"] | Literal["ground"],
    page: int = 1,
    limit: int = 10,
    timestamp: int | datetime | pd.Timestamp | str | None = "now",
    auth: None | Authentication = None,
) -> AirportList:
    """
    Fetch aircraft arriving, departing or on ground at a given airport.

    Returns on ground/scheduled/estimated/real times: see
    [fr24.types.fr24.FlightListItem][] for more details.

    :param client: HTTPX async client
    :param airport: IATA airport code (e.g. `HKG`)
    :param mode: arrivals, departures or on ground aircraft
    :param page: Page number
    :param limit: Number of results per page (max 100)
    :param timestamp: Show flights with STA before this Unix timestamp
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(timestamp)

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device

    params: AirportRequest = {
        "code": airport,
        "plugin[]": ["schedule"],
        "plugin-setting[schedule][mode]": mode,
        "page": page,
        "limit": limit,
    }

    if timestamp is not None:
        params["plugin-setting[schedule][timestamp]"] = timestamp

    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        params["token"] = auth["userData"]["subscriptionKey"]
    else:
        params["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/airport.json",
        headers=headers,
        params=params,  # type: ignore
    )

    response = await client.send(request)
    response.raise_for_status()
    return response.json()  # type: ignore


async def playback(
    client: httpx.AsyncClient,
    flight_id: int | str,
    timestamp: int | str | datetime | pd.Timestamp | None = None,
    auth: None | Authentication = None,
) -> Playback:
    """
    Fetch historical track playback data for a given flight.

    :param client: HTTPX async client
    :param flight_id: fr24 hex flight id
    :param timestamp: Unix timestamp (seconds) of ATD - optional, but
    it is recommended to include it
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(timestamp)
    if not isinstance(flight_id, str):
        flight_id = f"{flight_id:x}"

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device
    params: PlaybackRequest = {
        "flightId": flight_id,
    }
    if timestamp is not None:
        params["timestamp"] = timestamp
    if auth is not None and auth["userData"]["subscriptionKey"] is not None:
        params["token"] = auth["userData"]["subscriptionKey"]
    else:
        params["device"] = device

    request = httpx.Request(
        "GET",
        "https://api.flightradar24.com/common/v1/flight-playback.json",
        headers=headers,
        params=params,  # type: ignore[arg-type]
    )

    response = await client.send(request)
    response.raise_for_status()
    return response.json()  # type: ignore


def playback_metadata_dict(flight: FlightData) -> dict:  # type: ignore[type-arg]
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
    """
    return {
        "timestamp": point["timestamp"],
        "latitude": point["latitude"],
        "longitude": point["longitude"],
        "altitude": point["altitude"]["feet"],
        "ground_speed": point["speed"]["kts"],
        "vertical_speed": point["verticalSpeed"]["fpm"],
        "heading": point["heading"],
        "squawk": int(point["squawk"], base=8),
    }


def playback_track_ems_dict(point: TrackData) -> PlaybackTrackEMSRecord | None:
    """
    If the Extended Mode-S data is available in this observation,
    flatten and rename each variable to a dictionary. Otherwise, return `None`.
    """
    if e := point["ems"]:
        return {
            "timestamp": e["ts"],
            "ias": e["ias"],
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


# TODO: add ems, metadata.
def playback_df(result: Playback) -> pd.DataFrame:
    """
    Transform each point in the flight track to a pandas DataFrame.
    """
    flight = result["result"]["response"]["data"]["flight"]
    df = pd.DataFrame.from_records(
        playback_track_dict(point) for point in flight["track"]
    )

    df = df.eval(
        """
timestamp = @pd.to_datetime(timestamp, unit='s', utc=True)
    """
    )
    return df


def flight_list_dict(entry: FlightListItem) -> FlightListRecord:
    """
    Flatten a flight entry into dict, converting fr24 hex ids into integers.
    """
    orig = entry["airport"]["origin"]
    dest = entry["airport"]["destination"]
    icao24 = entry["aircraft"]["hex"]
    id_ = entry["identification"]["id"]
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
        "STOD": entry["time"]["scheduled"]["departure"],
        "ETOD": entry["time"]["estimated"]["departure"],
        "ATOD": entry["time"]["real"]["departure"],
        "STOA": entry["time"]["scheduled"]["arrival"],
        "ETOA": entry["time"]["estimated"]["arrival"],
        "ATOA": entry["time"]["real"]["arrival"],
    }


def flight_list_df(result: FlightList) -> None | pd.DataFrame:
    """
    Transform each flight entry in the JSON response into a pandas DataFrame.
    """
    list_ = result["result"]["response"]["data"]
    if list_ is None:
        return None
    df = pd.DataFrame.from_records(flight_list_dict(entry) for entry in list_)
    return df.eval(
        """
STOD = @pd.to_datetime(STOD, unit="s", utc=True)
ETOD = @pd.to_datetime(ETOD, unit="s", utc=True)
ATOD = @pd.to_datetime(ATOD, unit="s", utc=True)
STOA = @pd.to_datetime(STOA, unit="s", utc=True)
ETOA = @pd.to_datetime(ETOA, unit="s", utc=True)
ATOA = @pd.to_datetime(ATOA, unit="s", utc=True)
"""
    )
