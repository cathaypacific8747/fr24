from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Protocol, TypeVar

from typing_extensions import runtime_checkable

if TYPE_CHECKING:
    from pathlib import Path
    from typing import IO, Any

    import polars as pl
    from google.protobuf.message import Message
    from typing_extensions import Literal, TypeAlias

    import pandas as pd


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0"
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
    import pandas as pd

    if isinstance(timestamp, (str, datetime)):
        return int(pd.Timestamp(timestamp).timestamp())
    if isinstance(timestamp, pd.Timestamp):
        return int(timestamp.timestamp())
    return timestamp


class BarePath(Path):
    """A path to a file without an extension."""


SupportedFormats: TypeAlias = Literal["parquet", "csv"]


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
        if format == "parquet":
            suffix = ".parquet"
        elif format == "csv":
            suffix = ".csv"
        else:
            raise ValueError(f"unsupported format: `{format}`")

        file = file.with_suffix(suffix)
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
