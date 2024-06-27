from __future__ import annotations

import json
import secrets
from datetime import datetime
from typing import Literal

import httpx
import pyarrow as pa
from loguru import logger

import pandas as pd

from .common import DEFAULT_HEADERS, to_unix_timestamp
from .types.airport_list import AirportList, AirportRequest
from .types.authentication import Authentication
from .types.cache import (
    FlightListRecord,
    PlaybackTrackEMSRecord,
    PlaybackTrackRecord,
    flight_list_schema,
    playback_track_schema,
)
from .types.flight_list import FlightList, FlightListItem, FlightListRequest
from .types.playback import (
    Playback,
    PlaybackFlightData,
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
    :param limit: Number of results per page - use `100` if authenticated.
    :param timestamp: Show flights with ATD before this Unix timestamp
    :param auth: Authentication data
    """
    timestamp = to_unix_timestamp(timestamp)

    if reg is not None:
        key, value = "reg", reg
    elif flight is not None:
        key, value = "flight", flight
    else:
        raise TypeError(
            "expected one of `reg` or `flight` to be set, but both are `None`"
        )

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


def playback_metadata_dict(flight: PlaybackFlightData) -> dict:  # type: ignore[type-arg]
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
        is only available in [EMS][fr24.types.fr24.EMS] data.

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


def playback_arrow(data: Playback) -> pa.Table:
    """
    Parse each [fr24.types.fr24.TrackData][] in the API response into a
    pyarrow.Table. Also adds [fr24.types.fr24.FlightData][] into the
    schema's metadata with key `_flight`.

    If the response is empty, a warning is logged and an empty table is returned
    """
    flight = data["result"]["response"]["data"]["flight"]
    if len(track := flight["track"]) == 0:
        logger.warning("no data in response, table will be empty")
    return pa.Table.from_pylist(
        [
            {
                **playback_track_dict(point),
                "ems": playback_track_ems_dict(point),
            }
            for point in track
        ],
        schema=playback_track_schema.with_metadata(
            {
                "_flight": json.dumps(playback_metadata_dict(flight)).encode(
                    "utf-8"
                )
            }
        ),
    )


def playback_df(data: Playback) -> pd.DataFrame:
    """
    Parse each [fr24.types.fr24.TrackData][] in the API response into a
    pandas DataFrame. Also adds [fr24.types.fr24.FlightData][] into the
    DataFrame's `.attrs`.

    If the response is empty, a warning is logged and an empty table is returned
    """
    arr = playback_arrow(data)
    df: pd.DataFrame = arr.to_pandas()
    df.attrs = json.loads(arr.schema.metadata[b"_flight"])
    return df.eval(
        """
timestamp = @pd.to_datetime(timestamp, unit='s', utc=True)
    """
    )


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


def flight_list_arrow(data: FlightList) -> pa.Table:
    """
    Parse each [fr24.types.fr24.FlightListItem][] in the API response into a
    pyarrow.Table.

    If the response is empty, a warning is logged and an empty table is returned
    """
    flights = data["result"]["response"]["data"] or []
    if len(flights) == 0:
        logger.warning("no data in response, table will be empty")
    return pa.Table.from_pylist(
        [flight_list_dict(f) for f in flights],
        schema=flight_list_schema,
    )


def flight_list_df(data: FlightList) -> pd.DataFrame:
    """
    Parse each [fr24.types.fr24.FlightListItem][] in the API response into a
    pandas DataFrame.

    If the response is empty, a warning is logged and an empty table is returned
    """
    return flight_list_arrow(data).to_pandas()
