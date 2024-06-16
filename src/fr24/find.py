from __future__ import annotations

from typing import Any

import httpx
from typing_extensions import TypeGuard

from .types.find import (
    Aircraft,
    Airport,
    Entry,
    FindResult,
    Live,
    Operator,
    Schedule,
)


def is_airport(entry: Entry[Any]) -> TypeGuard[Entry[Airport]]:
    return entry["type"] == "airport"


def is_operator(entry: Entry[Any]) -> TypeGuard[Entry[Operator]]:
    return entry["type"] == "operator"


def is_live(entry: Entry[Any]) -> TypeGuard[Entry[Live]]:
    return entry["type"] == "live"


def is_schedule(entry: Entry[Any]) -> TypeGuard[Entry[Schedule]]:
    return entry["type"] == "schedule"


def is_aircraft(entry: Entry[Any]) -> TypeGuard[Entry[Aircraft]]:
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
