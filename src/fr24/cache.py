"""A simple file-based cache."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from appdirs import user_cache_dir

from .utils import BarePath, scan_table, to_flight_id, to_unix_timestamp

if TYPE_CHECKING:
    from typing import Callable, Generator

    import polars as pl
    from typing_extensions import Literal, TypeAlias

    from .utils import IntoFlightId, IntoTimestamp, SupportedFormats


PATH_CACHE = Path(user_cache_dir("fr24"))
if cache_path := os.environ.get("XDG_CACHE_HOME"):
    PATH_CACHE = Path(cache_path) / "fr24"


class FR24Cache:
    """
    - `flight_list/{kind}/{ident}`
    - `playback/{flight_id}`
    - `feed/{timestamp}`
    - `nearest_flights/{lon}_{lat}_{timestamp}`
    - `live_flights_status/{timestamp}`
    - `top_flights/{timestamp}`
    - `flight_details/{flight_id}_{timestamp}`
    - `playback_flight/{flight_id}_{timestamp}`
    """

    @classmethod
    def default(cls) -> FR24Cache:
        """
        Create a cache in the [default directory](../usage/cli.md#directories).
        """
        return cls(PATH_CACHE)

    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

        flight_list_dir = self.path / "flight_list"
        self.flight_list = FlightListBy(
            reg=Collection(flight_list_dir / "reg"),
            flight=Collection(flight_list_dir / "flight"),
        )
        self.playback = Collection(self.path / "playback")
        self.live_feed = Collection(self.path / "feed")
        self.nearest_flights = Collection(self.path / "nearest_flights")
        self.live_flights_status = Collection(self.path / "live_flights_status")
        self.top_flights = Collection(self.path / "top_flights")
        self.flight_details = Collection(self.path / "flight_details")
        self.playback_flight = Collection(self.path / "playback_flight")

        for collection in (
            self.flight_list.reg,
            self.flight_list.flight,
            self.playback,
            self.live_feed,
            self.nearest_flights,
            self.live_flights_status,
            self.top_flights,
            self.flight_details,
            self.playback_flight,
        ):
            collection.path.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class FlightListBy:
    reg: Collection
    """Collection of flight lists by registration number."""
    flight: Collection
    """Collection of flight lists by flight number."""

    def __call__(self, kind: Literal["reg", "flight"]) -> Collection:
        return getattr(self, kind)  # type: ignore


IntoIdent: TypeAlias = Any
"""An object that can be converted into an identifier for the cached file."""

Ident: TypeAlias = str
"""The identifier for the cached file."""


@dataclass(frozen=True)
class Collection:
    """A directory containing scannable files."""

    path: Path
    into_ident: Callable[[IntoIdent], Ident] = str

    def glob(self, pattern: str) -> Generator[File, None, None]:
        """
        Iterate over this collection and yield all scannable files matching
        the given relative pattern.
        """

        for fp in self.path.glob(pattern):
            yield File(fp)

    def scan_table(
        self,
        ident: File | Path | IntoIdent,
        *,
        format: SupportedFormats = "parquet",
    ) -> pl.LazyFrame:
        """
        Lazily load a file from this collection.

        :param ident: The path to the file to scan, or the identifier of the
            record in the collection:

            - `cache.flight_list.reg.scan_table`: Registration number, uppercase
            - `cache.flight_list.flight.scan_table`: Flight number, upper cased
            - `cache.playback.scan_table`: Flight id, hex representation,
                uppercase
            - `cache.feed.scan_table`: Unix timestamp, integer seconds since
                epoch
            - `cache.nearest_flights.scan_table`:
                `f"{int(longitude * 1e6)}_{int(latitude * 1e6)}_{timestamp}"`,
                where `longitude` and `latitude` are the coordinates in
                degrees, and `timestamp` is the integer seconds since epoch
            - `cache.live_flights_status.scan_table`: Unix timestamp,
                integer seconds since epoch
            - `cache.top_flights.scan_table`: Unix timestamp,
                integer seconds since epoch
            - `cache.flight_details.scan_table`:
                `f"{flight_id}_{timestamp}"`, where `flight_id` is the flight
                ID (hex representation, uppercase) and `timestamp` is the
                integer seconds since epoch
            - `cache.playback_flight.scan_table`:
                `f"{flight_id}_{timestamp}"`, where `flight_id` is the flight
                ID (hex representation, uppercase) and `timestamp` is
                actual time of departure, in integer seconds since epoch
        """
        if isinstance(ident, (File, Path)):
            file = ident
        else:
            file = self.new_bare_path(self.into_ident(ident))
        return scan_table(file, format=format)

    def new_bare_path(self, ident: str) -> BarePath:
        """
        Returns the bare path (without the file extension) to the file in this
        collection.
        """
        return BarePath(self.path / ident)


class File(Path):
    @property
    def format(self) -> SupportedFormats:
        # TODO: perform validation, though it is not critical
        return self.suffix[1:]  # type: ignore

    def scan(self) -> pl.LazyFrame:
        """Lazily load this file."""
        return scan_table(self, format=self.format)


def registration_number_to_ident(registration: str) -> Ident:
    return registration.upper()


def flight_number_to_ident(flight_number: str) -> Ident:
    return flight_number.upper()


def flight_id_to_ident(flight_id: IntoFlightId) -> Ident:
    return f"{to_flight_id(flight_id):0x}".upper()


def timestamp_to_ident(timestamp: IntoTimestamp) -> Ident:
    return str(to_unix_timestamp(timestamp))
