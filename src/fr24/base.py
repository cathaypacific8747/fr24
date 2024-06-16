from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, Literal, TypeVar

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
from loguru import logger
from typing_extensions import Self

import pandas as pd

from .authentication import login
from .types.fr24 import (
    Authentication,
    TokenSubscriptionKey,
    UsernamePassword,
)


class HTTPClient:
    """
    An HTTPX client for making requests to the API and storing
    authentication data.
    """

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.auth: Authentication | None = None

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


ApiRspRaw = TypeVar("ApiRspRaw")
"""Type returned by the API, e.g. [fr24.types.fr24.FlightList][]"""
Ctx = TypeVar("Ctx")
"""Type of the context for the service, a TypedDict"""


class APIBase(Generic[Ctx, ApiRspRaw], ABC):
    def __init__(self, http: HTTPClient) -> None:
        self.http = http

    @abstractmethod
    async def _fetch(
        self, ctx: Ctx, *args: Any, **kwargs: Any
    ) -> ApiRspRaw: ...


DType = TypeVar("DType")


class DataContainer(Generic[Ctx, DType]):
    def __init__(self, ctx: Ctx, data: DType) -> None:
        self.ctx: Ctx = ctx
        self.data: DType = data

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"ctx={self.ctx}, "
            f"data={self.data!r})"
        )


class APIRespBase(DataContainer[Ctx, ApiRspRaw], ABC):
    @abstractmethod
    def to_arrow(self) -> ArrowBase[Ctx]:
        """Parse API response and transform to arrow table."""


class ArrowBase(DataContainer[Ctx, pa.Table], ABC):
    """Wraps around pyarrow.Table with composition."""

    _default_schema: pa.Schema | None = None

    @classmethod
    @abstractmethod
    def _fp(cls, ctx: Ctx) -> Path:
        """Get path of parquet file given context."""

    @classmethod
    def _load(cls, ctx: Ctx) -> Self:
        fp = cls._fp(ctx)
        if not fp.exists():
            logger.warning(
                f"cannot find `{fp.stem}` in cache, creating an empty table"
            )
            return cls(
                ctx, pa.Table.from_pylist([], schema=cls._default_schema)
            )

        # enforce schema to match our version if defined.
        if (sch_d := cls._default_schema) is not None:
            sch = pq.read_schema(fp)
            if diffs := set(sch).difference(set(sch_d)):
                logger.warning(
                    f"cached file `{fp}` has unrecognized columns: {diffs}"
                )
                # TODO: in future versions, raise an error instead of casting.
                sch = sch.cast(sch)

            table = pq.read_table(fp, schema=sch)
        else:
            table = pq.read_table(fp)

        logger.debug(f"read {fp}: {table.num_rows=}")
        return cls(ctx, table)

    def concat(
        self, data_new: ArrowBase[Ctx], inplace: bool = False
    ) -> ArrowBase[Ctx]:
        logger.warning(
            "Using a non-overridden method to concatenate tables."
            "Context in the incoming table will be discarded."
        )
        table = pa.concat_tables([self.data, data_new.data])
        if inplace:
            self.data = table
            return self
        return self.__class__(self.ctx, table)

    def save(self, fp: Path | None = None) -> Self:
        """
        Write the arrow table to a parquet file in the cache directory.

        :param fp: The path to save the parquet file. If `None`, the
            cache directory will be used.
        """
        fp = self._fp(self.ctx)
        fp.parent.mkdir(parents=True, exist_ok=True)
        with pq.ParquetWriter(fp, schema=self.data.schema) as writer:
            writer.write_table(self.data)

        logger.debug(f"saved {self.data.num_rows} rows to {fp}")
        return self

    @property
    def df(self) -> pd.DataFrame:
        data = self.data.to_pandas()
        data.attrs = self.ctx
        return data


ApiBaseT = TypeVar("ApiBaseT")
"""`APIBase[ApiRsp]`"""
FileBaseT = TypeVar("FileBaseT")
"""`FileBase[ApiRsp]`"""


class ServiceBase(Generic[ApiBaseT, FileBaseT]):
    """A service to handle the API and disk operations."""

    def __init__(self, api: ApiBaseT, base_dir: Path) -> None:
        self._api = api
        self._base_dir = base_dir

    @abstractmethod
    async def fetch(
        self, *args: Any, **kwargs: Any
    ) -> APIRespBase[Ctx, ApiRspRaw]:
        """Fetch data from the API."""
        ...

    @abstractmethod
    def load(self, *args: Any, **kwargs: Any) -> ArrowBase[Ctx]:
        """Load data from disk."""
        ...
