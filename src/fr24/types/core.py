from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

from typing_extensions import NotRequired


class FlightListContext(TypedDict):
    ident: str
    kind: Literal["reg", "flight"]
    base_dir: NotRequired[Path]


class PlaybackContext(TypedDict):
    flight_id: str
    base_dir: NotRequired[Path]


class LiveFeedContext(TypedDict):
    timestamp: int
    source: Literal["live", "playback"]
    duration: NotRequired[int]
    hfreq: NotRequired[int]
    base_dir: NotRequired[Path]
