from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Protocol, TypeVar

from google.protobuf.message import Message
from typing_extensions import runtime_checkable

if TYPE_CHECKING:
    from typing import IO, Any

    import polars as pl
    from typing_extensions import TypeAlias

    import pandas as pd


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;"
    "q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    # TODO: use zstd instead - depend on httpx[zstd]
    "Origin": "https://www.flightradar24.com",
    "Connection": "keep-alive",
    "Referer": "https://www.flightradar24.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "TE": "trailers",
}


def to_unix_timestamp(
    timestamp: int | datetime | pd.Timestamp | str | Literal["now"] | None,
) -> int | None:
    """
    Casts timestamp-like object to a Unix timestamp in integer seconds,
    returning `None` if `timestamp` is `None`.
    """
    import pandas as pd

    if timestamp == "now":
        return int(time.time())
    if isinstance(timestamp, (str, datetime)):
        return int(pd.Timestamp(timestamp).timestamp())
    if isinstance(timestamp, pd.Timestamp):
        return int(timestamp.timestamp())
    if isinstance(timestamp, int):
        assert timestamp < 4102462800, (
            "timestamp should be in seconds, not milliseconds"
        )  # 2100-01-01
        return timestamp
    return None


class BarePath(Path):
    """A path to a file without an extension."""


SupportedFormats: TypeAlias = Literal["parquet", "csv"]


def format_bare_path(path: BarePath, format: SupportedFormats) -> BarePath:
    if format == "parquet":
        suffix = ".parquet"
    elif format == "csv":
        suffix = ".csv"
    else:
        raise ValueError(f"unsupported format: `{format}`")
    return path.with_suffix(suffix)


def write_table(
    result: SupportsToPolars,
    file: Path | IO[bytes] | BarePath,
    *,
    format: SupportedFormats = "parquet",
    **kwargs: Any,
) -> None:
    """
    Writes the table as the specified format via polars.

    :param file: File path or writable file-like object. The path will be given
        an appropriate suffix if it is a [BarePath][fr24.utils.BarePath].
    """

    if isinstance(file, BarePath):
        file = format_bare_path(file, format)
    if isinstance(file, Path):
        file.parent.mkdir(parents=True, exist_ok=True)

    data = result.to_polars()
    if format == "parquet":
        # NOTE: saving metadata with polars is not yet implemented
        # this means that useful unstructured metadata (e.g. flight details)
        # cannot be saved without extra pyarrow dependency
        # https://github.com/pola-rs/polars/issues/5117
        data.write_parquet(file, **kwargs)
    elif format == "csv":
        data.write_csv(file, **kwargs)
    else:
        raise ValueError(f"unsupported format: `{format}`")


def scan_table(
    file: Path | IO[bytes] | BarePath,
    *,
    format: SupportedFormats = "parquet",
) -> pl.LazyFrame:
    """
    Reads the table as the specified format via polars.

    :param file: File path or readable file-like object. The path will be given
        an appropriate suffix if it is a [BarePath][fr24.utils.BarePath].
    """
    import polars as pl

    if isinstance(file, BarePath):
        file = format_bare_path(file, format)

    if format == "parquet":
        return pl.scan_parquet(file)
    elif format == "csv":
        return pl.scan_csv(file)
    else:
        raise ValueError(f"unsupported format: `{format}`")


#
# important traits to perform conversions to other formats
# Into<TypedDict | google.protobuf.Message | pl.DataFrame>
# subclassing is not necessary, but recommended for static type checking
#

ProtoT_co = TypeVar("ProtoT_co", bound=Message, covariant=True)


@runtime_checkable
class SupportsToProto(Protocol[ProtoT_co]):
    def to_proto(self) -> ProtoT_co:
        """Converts the object into a protobuf message."""


DictT_co = TypeVar("DictT_co", covariant=True)
"""The dictionary representation of an object, e.g. `TypedDict`."""


@runtime_checkable
class SupportsToDict(Protocol[DictT_co]):
    def to_dict(self) -> DictT_co:
        """Converts the object into a dictionary."""


@runtime_checkable
class SupportsToPolars(Protocol):
    def to_polars(self) -> pl.DataFrame:
        """Converts the object into a polars dataframe."""
