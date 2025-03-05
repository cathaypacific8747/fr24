"""A simple file-based cache."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from appdirs import user_cache_dir

from .utils import BarePath, scan_table

if TYPE_CHECKING:
    from typing import Any, Generator

    import polars as pl
    from typing_extensions import Literal

    from .utils import SupportedFormats


PATH_CACHE = Path(user_cache_dir("fr24"))
if cache_path := os.environ.get("XDG_CACHE_HOME"):
    PATH_CACHE = Path(cache_path) / "fr24"


class Cache:
    """
    - `flight_list/{kind}/{ident}`
    - `playback/{flight_id}`
    - `feed/{timestamp}`
    """

    @classmethod
    def default(cls) -> Cache:
        """
        Create a cache in the [default directory](../usage/cli.md#directories).
        """
        return cls(PATH_CACHE)

    def __init__(self, path: Path) -> None:
        self.path = path

        flight_list_dir = path / "flight_list"
        self.flight_list = FlightListBy(
            reg=Collection(flight_list_dir / "reg"),
            flight=Collection(flight_list_dir / "flight"),
        )
        self.playback = Collection(path / "playback")
        self.live_feed = Collection(path / "feed")

        for collection in (
            self.flight_list.reg,
            self.flight_list.flight,
            self.playback,
            self.live_feed,
        ):
            collection.path.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class FlightListBy:
    reg: Collection
    flight: Collection

    def __call__(self, kind: Literal["reg", "flight"]) -> Collection:
        return getattr(self, kind)  # type: ignore


@dataclass(frozen=True)
class Collection:
    """A directory containing scannable files."""

    path: Path

    def glob(self, pattern: str) -> Generator[File, None, None]:
        """
        Iterate over this collection and yield all scannable files matching
        the given relative pattern.
        """

        for fp in self.path.glob(pattern):
            yield File(fp)

    def scan_table(
        self, ident: Any, *, format: SupportedFormats = "parquet"
    ) -> pl.LazyFrame:
        """
        - `cache.flight_list.reg`: Registration number, upper cased
        - `cache.flight_list.flight`: Flight number, upper cased
        - `cache.playback`: Flight id, hex representation
        - `cache.feed`: Unix Timestamp, integer seconds since epoch
        """
        return scan_table(self.new_bare_path(str(ident)), format=format)

    def new_bare_path(self, ident: str) -> BarePath:
        return BarePath(self.path / ident)


class File(Path):
    @property
    def format(self) -> SupportedFormats:
        # TODO: perform validation, though it is not critical
        return self.suffix[1:]  # type: ignore

    def scan(self) -> pl.LazyFrame:
        """Lazily load this file."""
        return scan_table(self, format=self.format)
