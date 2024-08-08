from __future__ import annotations

from datetime import datetime

import pandas as pd

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;"
    "q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://www.flightradar24.com",
    "Connection": "keep-alive",
    "Referer": "https://www.flightradar24.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}


def to_unix_timestamp(
    timestamp: int | datetime | pd.Timestamp | str | None,
) -> int | None:
    """
    Casts timestamp-like object to Unix timestamp,
    returning `None` if `timestamp` is `None`.
    """
    if isinstance(timestamp, (str, datetime)):
        return int(pd.Timestamp(timestamp).timestamp())
    if isinstance(timestamp, pd.Timestamp):
        return int(timestamp.timestamp())
    return timestamp
