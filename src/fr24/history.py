from __future__ import annotations

import secrets
from datetime import datetime
from typing import Literal

import httpx

import pandas as pd

from .common import DEFAULT_HEADERS
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
    if isinstance(timestamp, (str, datetime)):
        timestamp = pd.Timestamp(timestamp)
    if isinstance(timestamp, pd.Timestamp):
        timestamp = int(timestamp.timestamp())

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
        "timestamp": timestamp,
        "fetchBy": key,
        "page": page,
        "limit": limit,
    }

    if timestamp is None:
        del params["timestamp"]

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
    mode: Literal["arrivals"] | Literal["departures"],
    page: int = 1,
    limit: int = 10,
    timestamp: int | datetime | pd.Timestamp | str | None = "now",
    auth: None | Authentication = None,
) -> AirportList:
    if isinstance(timestamp, (str, datetime)):
        timestamp = pd.Timestamp(timestamp)
    if isinstance(timestamp, pd.Timestamp):
        timestamp = int(timestamp.timestamp())

    device = f"web-{secrets.token_urlsafe(32)}"
    headers = DEFAULT_HEADERS.copy()
    headers["fr24-device-id"] = device

    params: AirportRequest = {
        "code": airport,
        "plugin[]": ["schedule"],
        "plugin-setting[schedule][mode]": mode,
        "plugin-setting[schedule][timestamp]": timestamp,
        "page": page,
        "limit": limit,
    }

    if timestamp is None:
        del params["plugin-setting[schedule][timestamp]"]

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
    # NOTE: while `timestamp` is optional, we should always include it (ATOD)
    if isinstance(timestamp, (str, datetime)):
        timestamp = pd.Timestamp(timestamp, tz="utc")
    if isinstance(timestamp, pd.Timestamp):
        timestamp = int(timestamp.timestamp())
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
    ident = flight["identification"]
    sta = flight["status"]["generic"]
    owner = flight["owner"]
    airline = flight["airline"]
    origin = flight["airport"]["origin"]
    dest = flight["airport"]["destination"]
    return {
        "flight_id": int(ident["id"], 16),
        "callsign": ident["callsign"],
        "flight_number": ident["number"].get("default", None),
        "status_type": sta["status"]["type"],
        "status_text": sta["status"]["text"],
        "status_diverted": sta["status"]["diverted"],
        "status_time": int(sta["eventTime"]["utc"])
        if sta["eventTime"]["utc"]
        else None,
        "model_code": flight["aircraft"]["model"]["code"]
        if flight["aircraft"]
        else None,
        "icao24": int(flight["aircraft"]["identification"]["modes"], 16)
        if flight["aircraft"]
        else None,
        "registration": flight["aircraft"]["identification"]["registration"]
        if flight["aircraft"]
        else None,
        "owner": owner["code"]["icao"] if owner is not None else None,
        "airline": airline["code"]["icao"] if airline is not None else None,
        "origin": origin["code"]["icao"] if origin is not None else None,
        "destination": dest["code"]["icao"] if dest is not None else None,
        "median_delay": flight["median"]["delay"]
        if flight["median"]["delay"]
        else None,
        "median_time": int(flight["median"]["timestamp"])
        if flight["median"]["timestamp"]
        else None,
    }


def playback_track_dict(point: TrackData) -> PlaybackTrackRecord:
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
