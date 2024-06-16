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
    """An HTTPX client for making requests to the API."""

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


Ctx = TypeVar("Ctx")
"""Type of the context for the service, a TypedDict"""
ApiRspRaw = TypeVar("ApiRspRaw")
"""Type returned by the API, usually a TypedDict,
e.g. [fr24.types.fr24.FlightList][]"""


class APIResponse(Generic[Ctx, ApiRspRaw]):
    """Wraps an API response with context."""

    def __init__(self, ctx: Ctx, response: ApiRspRaw) -> None:
        self.ctx = ctx
        self.data = response

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ctx={self.ctx}, data={self.data})"


class ArrowTable(Generic[Ctx]):
    """Manages storage and retrieval of an arrow table with context."""

    def __init__(self, ctx: Ctx, table: pa.Table):
        # do not call directly. Use `from_file` instead.
        self.ctx = ctx
        self.data = table
        # self.schema = schema

    @classmethod
    def from_file(
        cls, ctx: Ctx, fp: Path, schema: pa.Schema | None = None
    ) -> Self:
        """Loads data from a parquet file, enforcing the schema if provided."""
        if not fp.exists():
            logger.warning(
                f"cannot find `{fp.stem}` in cache, "
                "creating an empty in-memory table"
            )
            return cls(ctx, pa.Table.from_pylist([], schema=schema))

        if (sch_d := schema) is not None:
            # enforce fp schema to match the provided.
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

    def concat(self, other: Self, inplace: bool = False) -> Self:
        # TODO: check if self.ctx != other.ctx:
        logger.warning(
            "Using a non-overridden method to concatenate tables."
            "Context in the incoming table will be discarded."
        )
        table = pa.concat_tables([self.data, other.data])
        if inplace:
            self.data = table
            return self
        return self.__class__(self.ctx, table)

    def save(self, fp: Path) -> Self:
        """Saves the table to a parquet file, with the schema if defined."""
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


class ServiceBase(ABC):
    """A service to handle the API and disk operations."""

    @abstractmethod
    async def fetch(self, *args: Any, **kwargs: Any) -> APIResponse[Any, Any]:
        """Fetches data from the API."""

    @abstractmethod
    def load(self, *args: Any, **kwargs: Any) -> ArrowTable[Any]:
        """Loads data from storage."""
