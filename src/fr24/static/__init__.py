import json
from pathlib import Path

import httpx

from ..common import DEFAULT_HEADERS
from ..types.static import AircraftFamily, Airlines, Airports, Countries

# filenames are based on indexeddb names
base_dir = Path(__file__).parent
AIRCRAFT_FAMILY_PATH = base_dir / "AircraftFamily.json"
AIRPORTS_PATH = base_dir / "Airports.json"
AIRLINES_PATH = base_dir / "Airlines.json"
COUNTRIES_PATH = base_dir / "MobileCountries.json"

DEFAULT_HEADERS_STATIC = {
    **DEFAULT_HEADERS,
    "Accept": "*/*",
}


async def fetch_aircraft_family(client: httpx.AsyncClient) -> AircraftFamily:
    request = httpx.Request(
        "GET",
        "https://www.flightradar24.com/mobile/aircraft-family",
        headers=DEFAULT_HEADERS_STATIC,
    )
    data = await client.send(request)
    data.raise_for_status()
    return data.json()


async def fetch_airlines(client: httpx.AsyncClient) -> Airlines:
    request = httpx.Request(
        "GET",
        "https://www.flightradar24.com/mobile/airlines",
        headers=DEFAULT_HEADERS_STATIC,
    )
    data = await client.send(request)
    data.raise_for_status()
    return data.json()


async def fetch_airports(
    client: httpx.AsyncClient, major_version: int = 4, minor_version: int = 0
) -> Airports:
    request = httpx.Request(
        "GET",
        f"https://www.flightradar24.com/mobile/airports/format/{major_version}",
        params={"version": minor_version},
        headers=DEFAULT_HEADERS_STATIC,
    )
    data = await client.send(request)
    data.raise_for_status()
    return data.json()


async def fetch_countries(client: httpx.AsyncClient) -> Countries:
    request = httpx.Request(
        "GET",
        "https://www.flightradar24.com/mobile/countries",
        headers=DEFAULT_HEADERS_STATIC,
    )
    data = await client.send(request)
    data.raise_for_status()
    return data.json()


async def update_all():
    async with httpx.AsyncClient(http2=True) as client:

        async def update(path, fetch_fn):
            with open(path, "w") as f:
                data = await fetch_fn(client)
                json.dump(data, f, indent=2)

        await update(AIRCRAFT_FAMILY_PATH, fetch_aircraft_family)
        await update(AIRPORTS_PATH, fetch_airports)
        await update(AIRLINES_PATH, fetch_airlines)
        await update(COUNTRIES_PATH, fetch_countries)


def get_aircraft_family() -> AircraftFamily:
    with open(AIRCRAFT_FAMILY_PATH, "r") as f:
        return json.load(f)


def get_airlines() -> Airlines:
    with open(AIRLINES_PATH, "r") as f:
        return json.load(f)


def get_airports() -> Airports:
    with open(AIRPORTS_PATH, "r") as f:
        return json.load(f)


def get_countries() -> Countries:
    with open(COUNTRIES_PATH, "r") as f:
        return json.load(f)
