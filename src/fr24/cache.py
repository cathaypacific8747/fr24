"""A simple file-based cache."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from appdirs import user_cache_dir

if TYPE_CHECKING:
    from typing_extensions import Literal


PATH_CACHE = Path(user_cache_dir("fr24"))
if cache_path := os.environ.get("XDG_CACHE_HOME"):
    PATH_CACHE = Path(cache_path) / "fr24"


@dataclass
class Cache:
    """
    - `flight_list/{kind}/{ident}`
    - `playback/{flight_id}`
    - `feed/{timestamp}`
    """

    base_dir: Path

    def __post_init__(self) -> None:
        for path in (
            self._flight_list_path("reg"),
            self._flight_list_path("flight"),
            self._playback_path(),
            self._feed_path(),
        ):
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def default(cls) -> Cache:
        """
        Create a cache in the [default directory](../usage/cli.md#directories).
        """
        return cls(PATH_CACHE)

    def _flight_list_path(self, kind: Literal["reg", "flight"]) -> Path:
        return self.base_dir / "flight_list" / kind

    def _playback_path(self) -> Path:
        return self.base_dir / "playback"

    def _feed_path(self) -> Path:
        return self.base_dir / "feed"
