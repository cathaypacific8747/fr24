from __future__ import annotations

from typing import Literal, TypedDict


class FlightListContext(TypedDict):
    reg: str | None
    flight: str | None


class PlaybackContext(TypedDict):
    flight_id: str


class LiveFeedContext(TypedDict):
    timestamp: int | None
    source: Literal["live", "playback"]
    duration: int | None
    hfreq: int | None
