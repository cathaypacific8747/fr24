from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

import httpx
import pyarrow as pa
import pyarrow.parquet as pq
from loguru import logger
from typing_extensions import Self

import pandas as pd

from .authentication import login
from .types.fr24 import Authentication


class HTTPClient:
    """
    An HTTPX client for making requests to the API and storing
    authentication data.
    """

    def __init__(self, *, retries: int = 5) -> None:
        transport = httpx.AsyncHTTPTransport(retries=retries)
        self.client = httpx.AsyncClient(transport=transport)
        self.auth: Authentication | None = None

    async def __aenter__(self) -> Self:
        self.auth = await login(self.client)
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self.client is not None:
            await self.client.aclose()


ApiRsp = TypeVar("ApiRsp")
"""Type returned by the API, e.g. [fr24.types.fr24.FlightList][]"""
Ctx = TypeVar("Ctx")
"""Type of the context for the service, a TypedDict"""


class APIBase(Generic[ApiRsp, Ctx], ABC):
    def __init__(self, http: HTTPClient, ctx: Ctx) -> None:
        self.http = http
        self.ctx = ctx

    @abstractmethod
    async def fetch(self, *args: Any, **kwargs: Any) -> ApiRsp:
        """Fetch data from the API."""
        ...


class ArrowBase(Generic[ApiRsp, Ctx], ABC):
    """A base class for handling arrow tables."""

    schema: pa.Schema | None = None

    def __init__(self, base_dir: str, ctx: Ctx) -> None:
        self.base_dir = Path(base_dir)
        self._table: pa.Table | None = None
        self.ctx = ctx

    @property
    @abstractmethod
    def fp(self) -> Path:
        """Path to the parquet file."""
        ...

    @property
    def table(self) -> pa.Table | None:
        return self._table

    @table.setter
    def table(self, table: pa.Table) -> None:
        """Set the arrow table or extend it if it already exists."""
        self._table = (
            table
            if self._table is None
            else self._concat_tables(self._table, table)
        )

    @staticmethod
    def _concat_tables(tbl_old: pa.Table, tbl_new: pa.Table) -> pa.Table:
        """Override this to customize how tables should be concatenated."""
        return pa.concat_tables([tbl_old, tbl_new])

    @abstractmethod
    def add_api_response(self, data: ApiRsp) -> Self:
        """Parse API response and add to the arrow table."""

    def add_parquet(self, fp: Path | None = None) -> Self:
        """
        Read parquet file and add to the arrow table.

        :param fp: Path to the parquet file - if not provided, the default cache
        directory is used.
        """
        out_fp = fp if fp is not None else self.fp

        # pq.read_table apparently doesn't read schema metadata:
        # overwriting self.schema using pq.read_schema instead.
        sch = pq.read_schema(out_fp)
        if sch_diffs := set(sch).difference(set(self.schema or [])):
            # TODO: find a better way to cast the new schema into this schema
            # raise_for_status?
            logger.warning(f"Schema mismatch: {sch_diffs}")
            sch = sch.cast(self.schema)  # attempt to cast the schema
        self.schema = sch

        self.table = pq.read_table(out_fp, **self._schema_kwargs)
        num_rows = self._table.num_rows if self._table is not None else 0
        logger.debug(f"Read {out_fp}: {num_rows=}")
        return self

    def save_parquet(self, fp: Path | None = None) -> Self:
        """
        Write the arrow table to a parquet file.
        :param fp: Path to the parquet file - if not provided, the default cache
        directory is used.
        """
        if self._table is None:
            logger.warning("No data to write.")
            return self
        out_fp = fp if fp is not None else self.fp
        out_fp.parent.mkdir(parents=True, exist_ok=True)
        with pq.ParquetWriter(out_fp, **self._schema_kwargs) as writer:
            writer.write_table(self._table)
        logger.debug(f"Saved {self._table.num_rows} rows to {out_fp}")
        return self

    def clear(self) -> None:
        """Clear the arrow table."""
        self._table = None

    @property
    def _schema_kwargs(self) -> dict[str, Any]:
        return {} if self.schema is None else {"schema": self.schema}

    @property
    def df(self) -> pd.DataFrame | None:
        return self._table.to_pandas() if self._table is not None else None


ApiBaseT = TypeVar("ApiBaseT")
"""`APIBase[ApiRsp]`"""
FileBaseT = TypeVar("FileBaseT")
"""`FileBase[ApiRsp]`"""


class ServiceBase(Generic[ApiBaseT, FileBaseT, Ctx]):
    """A service to handle the API and file operations."""

    def __init__(self, api: ApiBaseT, data: FileBaseT, ctx: Ctx) -> None:
        self.api = api
        self.data = data
        self.ctx = ctx
