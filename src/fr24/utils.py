from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Generic,
    Literal,
    Protocol,
    TypeVar,
    Union,
)

from typing_extensions import runtime_checkable

if TYPE_CHECKING:
    from typing import IO, Any, NoReturn

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


T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Ok(Generic[T]):
    __slots__ = ("_value",)  # py39 compat
    _value: T

    def ok(self) -> T:
        return self._value

    def err(self) -> None:
        return None

    def is_ok(self) -> Literal[True]:
        return True

    def is_err(self) -> Literal[False]:
        return False

    def unwrap(self) -> T:
        return self._value


@dataclass(frozen=True)
class Err(Generic[E]):
    __slots__ = ("_value",)
    _value: E

    def ok(self) -> None:
        return None

    def err(self) -> E:
        return self._value

    def is_ok(self) -> Literal[False]:
        return False

    def is_err(self) -> Literal[True]:
        return True

    def unwrap(self) -> NoReturn:
        raise UnwrapError(
            self, f"called `Result.unwrap()` on errored result: {self._value!r}"
        )


class UnwrapError(Exception):
    def __init__(self, err: Any, message: str) -> None:
        self._err = err
        super().__init__(message)

    @property
    def err(self) -> Any:
        return self._err


Result: TypeAlias = Union[Ok[T], Err[E]]
"""A type that represents either success (`Ok`) or failure (`Err`)."""
