from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Generic,
    Protocol,
    TypeVar,
)

import httpx
import polars as pl
from google.protobuf.message import Message
from typing_extensions import runtime_checkable

from .authentication import login

if TYPE_CHECKING:
    from typing import IO, Any, Literal

    import httpx
    from typing_extensions import Self

    from .types.authentication import (
        Authentication,
        TokenSubscriptionKey,
        UsernamePassword,
    )

#
# api
#


@dataclass
class HTTPClient:
    """An HTTPX client for making requests to the API."""

    client: httpx.AsyncClient
    auth: Authentication | None = None

    async def _login(
        self,
        creds: (
            TokenSubscriptionKey | UsernamePassword | Literal["from_env"] | None
        ) = "from_env",
    ) -> None:
        self.auth = await login(self.client, creds)

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self.client is not None:
            await self.client.aclose()


RequestT = TypeVar("RequestT")
"""Arguments for the request"""


@dataclass
class APIResult(Generic[RequestT]):
    """Wraps raw bytes with context."""

    request: RequestT
    response: httpx.Response


@runtime_checkable
class Fetchable(Protocol, Generic[RequestT]):
    async def fetch(self, *args: Any, **kwargs: Any) -> APIResult[RequestT]:
        """Fetches data from the API."""


#
# converters
#


DictT_co = TypeVar("DictT_co", covariant=True)
"""The dictionary representation of the raw bytes, e.g. `TypedDict`."""


@runtime_checkable
class SupportsToDict(Protocol, Generic[DictT_co]):
    def to_dict(self) -> DictT_co:
        """Converts the raw bytes to a dictionary."""


ProtoT_co = TypeVar("ProtoT_co", bound=Message, covariant=True)


@runtime_checkable
class SupportsToProto(Protocol, Generic[ProtoT_co]):
    def to_proto(self) -> ProtoT_co:
        """Converts the raw bytes to a protobuf message."""


@runtime_checkable
class SupportsToPolars(Protocol):
    def to_polars(self) -> pl.DataFrame:
        """Converts the raw bytes to a polars dataframe."""


#
# file system
#


@runtime_checkable
class HasFilePath(Protocol):
    base_dir: Path

    @property
    def file_path(cls) -> Path:
        """
        Returns the default file path for the given context, without the file
        extension.
        """


class CacheMixin(HasFilePath, SupportsToPolars):
    def save(
        self,
        file: Path | IO[bytes] | None = None,
        *,
        format: Literal["parquet", "csv"] = "parquet",
    ) -> Self:
        """
        Writes the table as the specified format via polars.

        For more granular control, use `to_polars` and `_file_path`.

        :param file: The path of a file or a file-like object write to,
            e.g. `sys.stdout.buffer`.
        """
        file = file or self.file_path
        if isinstance(file, Path):
            file.parent.mkdir(parents=True, exist_ok=True)

        data = self.to_polars()
        if format == "parquet":
            if isinstance(file, Path):
                file = file.with_suffix(".parquet")
            data.write_parquet(file)
        elif format == "csv":
            if isinstance(file, Path):
                file = file.with_suffix(".csv")
            data.write_csv(file)
        else:
            raise ValueError(f"unsupported format: `{format}`")

        return self


# def load(cls, *args, **args) -> Any:

# def glob_cache(cls, pattern: str) -> list[Path]:
#     """Returns a list of cached files matching the given pattern."""

# def scan_cache(cls, pattern: str) -> pl.LazyFrame:
#     """
#     Returns a lazy dataframe of cached files matching the given pattern.
#     """
