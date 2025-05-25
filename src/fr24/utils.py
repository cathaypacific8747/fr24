from __future__ import annotations

import logging
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

IntoTimestamp: TypeAlias = Union[int, datetime]
"""Unix timestamp in seconds or a datetime object."""


def to_unix_timestamp(
    timestamp: IntoTimestamp | str | Literal["now"] | None,
) -> int | Literal["now"] | None:
    """Casts timestamp-like object to a Unix timestamp in integer seconds,
    returning `None` if `timestamp` is `None`.
    """
    if isinstance(timestamp, str):
        # TODO(abrah): should we eagerly return the current timestamp just like
        # `pd.Timestamp("now")`? we might want to defer this to the caller.
        if timestamp == "now":
            return "now"
        import polars as pl

        dt: datetime = pl.Series(values=(timestamp,)).str.to_datetime().item(0)
        return int(dt.timestamp())
    if isinstance(timestamp, datetime):
        return int(timestamp.timestamp())
    if isinstance(timestamp, int):
        assert timestamp < 4102462800, (
            "timestamp should be in seconds, not milliseconds"
        )  # 2100-01-01
        return timestamp
    return None


def get_current_timestamp() -> int:
    """Returns the current Unix timestamp in seconds."""
    return int(time.time())


IntoFlightId: TypeAlias = Union[int, str, bytes]


def to_flight_id(flight_id: IntoFlightId) -> int:
    if isinstance(flight_id, (str, bytes)):
        return int(flight_id, 16)
    return flight_id


class BarePath(Path):
    """A path to a file without an extension."""


SupportedFormats: TypeAlias = Literal["parquet", "csv"]  # TODO: support ndjson


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
    file: str | Path | IO[bytes] | BarePath,
    *,
    format: SupportedFormats = "parquet",
    **kwargs: Any,
) -> None:
    """Writes the table as the specified format via polars.

    :param file: File path or writable file-like object. The path will be given
        an appropriate suffix if it is a [BarePath][fr24.utils.BarePath].
    """

    if isinstance(file, BarePath):
        file = format_bare_path(file, format)
    if isinstance(file, str):
        file = Path(file)
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


# In the json api, the httpx.Response class stores the response body AND any
# errors in the same object. For example, `response.json()` effectively tries to
# parse the response body as JSON, and if it fails, raises an error.
# We want to mirror this behaviour in the gRPC api, so we define a Result type
# that can be *either* a successful parsed protocol buffer or a gRPC error.

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


# for use in tests
def intercept_logs_with_loguru(
    level: logging._Level = logging.INFO, modules: tuple[str, ...] = ()
) -> None:
    """Intercepts stdlib logging to stderr with loguru.

    :param level: The stdlib logging level to intercept.
    :param modules: The modules to intercept.
    """
    import inspect
    from itertools import chain

    from loguru import logger

    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            # Get corresponding Loguru level if it exists.
            try:
                level: str | int = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message.
            frame, depth = inspect.currentframe(), 0
            while frame:
                filename = frame.f_code.co_filename
                is_logging = filename == logging.__file__
                is_frozen = "importlib" in filename and "_bootstrap" in filename
                if depth > 0 and not (is_logging or is_frozen):
                    break
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.basicConfig(handlers=[InterceptHandler()], level=level, force=True)
    for logger_name in chain(("",), modules):
        logger_module = logging.getLogger(logger_name)
        logger_module.handlers = [InterceptHandler(level=level)]
        logger_module.propagate = False
