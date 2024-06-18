from __future__ import annotations

from pathlib import Path
from typing import Literal, TypedDict

from typing_extensions import NotRequired

from .fr24 import LivefeedField


# internally tagged
class FlightListContext(TypedDict):
    ident: str
    kind: Literal["reg", "flight"]
    base_dir: NotRequired[Path]


class PlaybackContext(TypedDict):
    flight_id: str
    base_dir: NotRequired[Path]


class LiveFeedContext(TypedDict):
    timestamp: int | None
    source: Literal["live", "playback"]
    duration: NotRequired[int | None]
    hfreq: NotRequired[int | None]
    limit: NotRequired[int | None]
    fields: NotRequired[list[LivefeedField] | None]
    base_dir: NotRequired[Path]
