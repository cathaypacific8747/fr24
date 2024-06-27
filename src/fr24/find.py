from __future__ import annotations

import httpx
from typing_extensions import TypeGuard

from .types.find import (
    AircraftEntry,
    AirportEntry,
    Entry,
    FindResult,
    LiveEntry,
    OperatorEntry,
    ScheduleEntry,
)


def is_airport(entry: Entry) -> TypeGuard[AirportEntry]:
    return entry["type"] == "airport"


def is_operator(entry: Entry) -> TypeGuard[OperatorEntry]:
    return entry["type"] == "operator"


def is_live(entry: Entry) -> TypeGuard[LiveEntry]:
    return entry["type"] == "live"


def is_schedule(entry: Entry) -> TypeGuard[ScheduleEntry]:
    return entry["type"] == "schedule"


def is_aircraft(entry: Entry) -> TypeGuard[AircraftEntry]:
    return entry["type"] == "aircraft"


async def find(client: httpx.AsyncClient, query: str) -> None | FindResult:
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
    if response.status_code != 200:
        return None
    return response.json()  # type: ignore
