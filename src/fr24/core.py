from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
)

import httpx
from typing_extensions import Self

from . import PATH_CACHE
from .base import (
    APIResult,
    CacheMixin,
    Fetchable,
    HTTPClient,
    SupportsToDict,
)

# from .grpc import (
#     live_feed_playback_world_data,
#     live_feed_world_data,
# )
from .json import (
    FlightListRequest,
    PlaybackRequest,
    flight_list,
    flight_list_df,
    flight_list_parse,
    playback,
    playback_df,
    playback_metadata_dict,
    playback_parse,
)
from .types import overwrite_args_signature_from
from .types.flight_list import FlightList
from .types.playback import Playback

if TYPE_CHECKING:
    from typing import (
        AsyncIterator,
        Literal,
    )

    import polars as pl

    from .types.authentication import TokenSubscriptionKey, UsernamePassword

    # from .types.cache import (
    #     LiveFeed,
    #     flight_list_schema,
    #     live_feed_schema,
    #     playback_track_schema,
    # )
    # from .types.core import (
    #     LiveFeedContext,
    # )
    from .types.fr24 import LiveFeedField
    # from .types.playback import FlightData


# NOTE: saving metadata with polars is unfortunately not yet implemented
# https://github.com/pola-rs/polars/issues/5117


class FR24:
    def __init__(
        self,
        client: httpx.AsyncClient | None = None,
        *,
        base_dir: Path | str = PATH_CACHE,
    ) -> None:
        """
        See docs [quickstart](../usage/quickstart.md#initialisation).

        :param client: The `httpx` client to use. If not provided, a
            new one will be created with HTTP/2 enabled by default. It is
            highly recommended to use `http2=True` to avoid
            [464 errors](https://github.com/cathaypacific8747/fr24/issues/23#issuecomment-2125624974)
            and to be consistent with the browser.
        :param base_dir:
            See [cache directory](../usage/cli.md#directories).
        """
        self.http = HTTPClient(
            httpx.AsyncClient(http2=True) if client is None else client
        )
        """The HTTP client for use in requests"""
        self.__base_dir = Path(base_dir)

        factory = ServiceFactory(self.http, self.base_dir)
        self.flight_list = factory.build_flight_list()
        """Flight list service."""
        self.playback = factory.build_playback()
        """Playback service."""
        self.live_feed = factory.build_live_feed()
        """Live feed service."""

    async def login(
        self,
        creds: (
            TokenSubscriptionKey | UsernamePassword | None | Literal["from_env"]
        ) = "from_env",
    ) -> None:
        """
        :param creds: Reads credentials from the environment variables or the
            config file if `creds` is set to `"from_env"` (default). Otherwise,
            provide the credentials directly.
        """
        await self.http._login(creds)

    @property
    def base_dir(self) -> Path:
        """The [cache directory](../usage/cli.md#directories)."""
        return self.__base_dir

    async def __aenter__(self) -> Self:
        await self.http.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.http.__aexit__(*args)


@dataclass
class ServiceFactory:
    http: HTTPClient
    base_dir: Path

    def build_flight_list(self) -> FlightListService:
        return FlightListService(self)

    def build_playback(self) -> PlaybackService:
        return PlaybackService(self)

    def build_live_feed(self) -> LiveFeedService:
        return LiveFeedService(self)


@dataclass(frozen=True)
class FlightListService(Fetchable[FlightListRequest]):
    """Flight list service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(FlightListRequest)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> FlightListResult:
        """
        Fetch the flight list.
        See [fr24.json.FlightListRequest][] for the detailed signature.
        """
        request = FlightListRequest(*args, **kwargs)
        response = await flight_list(
            self.__factory.http.client,
            request,
            self.__factory.http.auth,
        )
        return FlightListResult(
            request=FlightListRequest(*args, **kwargs),
            response=response,
            base_dir=self.__factory.base_dir,
        )

    @dataclass
    class FetchAllArgs(FlightListRequest):
        """Arguments for fetching all pages of the flight list."""

        delay: int = field(default=5)

    @overwrite_args_signature_from(FetchAllArgs)
    async def fetch_all(
        self, /, *args: Any, **kwargs: Any
    ) -> AsyncIterator[FlightListResult]:
        """
        Fetch all pages of the flight list.

        See [fr24.core.FlightListService.FetchAllArgs][] for the detailed
        signature.
        """
        # TODO: something nasty with async generators is happening here
        # (httpx leak)
        more = True
        page = kwargs.get("page", 1)
        delay = kwargs.pop("delay", 5)
        while more:
            kwargs["page"] = page
            response = await self.fetch(*args, **kwargs)

            response_dict = response.to_dict()
            # shouldn't happen, but stop in case we overshot
            if (data := response_dict["result"]["response"]["data"]) is None:
                break
            yield response
            page += 1

            # NOTE: for the next request, we have to both:
            # - update the timestamp to the earliest STD in the current batch
            # - increment the page
            # weird, but it's how the API works
            timestamp = min(
                t
                for d in data
                if (t := d["time"]["scheduled"]["departure"]) is not None
            )
            kwargs["timestamp"] = timestamp

            more = response_dict["result"]["response"]["page"]["more"]
            await asyncio.sleep(delay)


#     @override
#     def concat(
#         self,
#         data_new: FlightListArrow,
#         inplace: bool = False,
#     ) -> FlightListArrow:
#         """
#         Returns a new list of flights merged with the current table.
#         Duplicates are removed from the current table, which results in
#         all `Estimated` flights to be updated with the new data (if any).

#         :param inplace: If `True`, the current table will be updated in place.
#         """
#         # NOTE: not using `flight_id` as primary key as it is nullable
#         mask: pa.ChunkedArray = pc.is_in(
#             self.data["STOD"], value_set=data_new.data["STOD"]
#         )
#         if (dup_count := pc.sum(mask).as_py()) is not None and dup_count > 0:
#             logger.info(f"overwriting {dup_count} duplicate flight ids")
#         data = pa.concat_tables(
#             [self.data.filter(pc.invert(mask.combine_chunks())), data_new.data]
#         )
#         if inplace:
#             self.data = data
#             return self
#         return FlightListArrow(self.ctx, data)


@dataclass
class FlightListResult(
    APIResult[FlightListRequest],
    SupportsToDict[FlightList],
    CacheMixin,
):
    base_dir: Path

    def to_dict(self) -> FlightList:
        return flight_list_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return flight_list_df(self.to_dict())

    @property
    def file_path(self) -> Path:
        return (
            self.base_dir
            / "flight_list"
            / self.request.kind
            / f"{self.request.ident.upper()}"
        )


@dataclass(frozen=True)
class PlaybackService(Fetchable[PlaybackRequest]):
    """Playback service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(PlaybackRequest)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> PlaybackResult:
        """
        FIXME - add docs
        See [fr24.json.PlaybackRequest][] for the detailed signature.
        """
        request = PlaybackRequest(*args, **kwargs)
        response = await playback(
            self.__factory.http.client,
            request,
            self.__factory.http.auth,
        )
        return PlaybackResult(
            request=PlaybackRequest(*args, **kwargs),
            response=response,
            base_dir=self.__factory.base_dir,
        )

    @classmethod
    def metadata(cls, response_dict: Playback) -> dict[str, Any]:
        return playback_metadata_dict(
            response_dict["result"]["response"]["data"]["flight"]
        )


@dataclass
class PlaybackResult(
    APIResult[PlaybackRequest],
    SupportsToDict[Playback],
    CacheMixin,
):
    base_dir: Path

    def to_dict(self) -> Playback:
        return playback_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return playback_df(self.to_dict())

    @property
    def file_path(self) -> Path:
        return self.base_dir / "playback" / str(self.request.flight_id)


#     @property
#     def metadata(self) -> FlightData | None:
#         """Parse the flight metadata from the arrow table."""
#         if m := self.data.schema.metadata.get(b"_flight"):
#             return json.loads(m)  # type: ignore[no-any-return]
#         return None


# NOTE: putting here temporarily because namespace clash at .grpc.
@dataclass
class LiveFeedRequest:
    timestamp: int | None
    source: Literal["live", "playback"]
    # FIXME: below should have defaults
    duration: int | None
    hfreq: int | None
    limit: int | None
    fields: list[LiveFeedField] | None
    base_dir: Path


@dataclass(frozen=True)
class LiveFeedService(Fetchable[LiveFeedRequest]):
    """Playback service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(LiveFeedRequest)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> LiveFeedResult:
        """
        Fetch the flight list.
        See [fr24.grpc.LiveFeedRequest][] for the detailed signature.
        """
        request = LiveFeedRequest(*args, **kwargs)
        response = await playback(  # FIXME
            self.__factory.http.client,
            request,
            self.__factory.http.auth,
        )
        return LiveFeedResult(
            request=LiveFeedRequest(*args, **kwargs),
            response=response,
            base_dir=self.__factory.base_dir,
        )


@dataclass
class LiveFeedResult(
    APIResult[LiveFeedRequest],
    SupportsToDict[dict[str, Any]],  # FIXME
    CacheMixin,
):
    base_dir: Path

    def to_dict(self) -> dict[str, Any]:  # FIXME
        return live_feed_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return live_feed_df(self.to_dict())

    @property
    def file_path(self) -> Path:
        return self.base_dir / "feed" / str(self.request.timestamp)


# class LiveFeedAPI:
#     def __init__(self, http: HTTPClient) -> None:
#         self.http = http

#     async def _fetch(
#         self,
#         ctx: LiveFeedContext,
#     ) -> list[LiveFeedRecord]:
#         kw = {
#             k: v
#             for k, v in ctx.items()
#             if k in ("limit", "fields") and v is not None
#         }
#         if (ts := ctx["timestamp"]) is not None:
#             kw.update(
#                 {
#                     k: v
#                     for k, v in ctx.items()
#                     if k in ("duration", "hfreq") and v is not None
#                 }
#             )
#             return await live_feed_playback_world_data(
#                 self.http.client,
#                 ts,
#                 **kw,  # type: ignore[arg-type]
#                 auth=self.http.auth,
#             )
#         resp = await live_feed_world_data(
#             self.http.client,
#             self.http.auth,
#             **kw,  # type: ignore[arg-type]
#         )
#         ctx["timestamp"] = int(time.time())
#         # TODO: use server time instead, but it doesn't really matter because
#         # live feed messages have timestamps attached to them anyway
#         return resp


# class LiveFeedArrow(ArrowTable[LiveFeedContext]):
#     """Arrow table for live feed data."""

#     @classmethod
#     def from_cache(cls, ctx: LiveFeedContext) -> LiveFeedArrow:
#         fp = LiveFeedArrow._fp(ctx)
#         return super(LiveFeedArrow, cls).from_file(ctx, fp, live_feed_schema)

#     @classmethod
#     def _fp(cls, ctx: LiveFeedContext) -> Path:
#         ts = ctx["timestamp"]
#         assert ts is not None, (
#             "tried to get a cached snapshot of the live feed, but the "
#             "timestamp was not provided."
#         )
#         return ctx["base_dir"] / "feed" / f"{ts}.parquet"

#     @override
#     def concat(
#         self, data_new: LiveFeedArrow, inplace: bool = False
#     ) -> LiveFeedArrow:
#         raise NotImplementedError(
#             "live feed data cannot be concatenated together"
#         )

#     @override
#     def save(
#         self,
#         fp: Path | BinaryIO | None = None,
#         fmt: Literal["parquet", "csv"] = "parquet",
#     ) -> Self:
#         """
#         Write the table to the given file path or file-like object,
#         e.g. `./tmp/foo.parquet`, `sys.stdout`.

#         :param fp: File path to save the table to. If `None`, the table will
#             be saved to the appropriate cache directory.

#         :raises ValueError: If a format other than `parquet` is provided when
#             saving to cache.
#         """
#         if fp is None and fmt != "parquet":
#             raise ValueError("format must be `parquet` when saving to cache")
#         super().save(fp if fp is not None else LiveFeedArrow._fp(self.ctx), fmt)
#         return self


# class LiveFeedService(ServiceBase):
#     """A service to handle the live feed API and file operations."""

#     def __init__(self, http: HTTPClient, base_dir: Path) -> None:
#         self._http = http
#         self._base_dir = base_dir
#         self._api = LiveFeedAPI(http)

#     async def fetch(
#         self,
#         timestamp: int | str | datetime | pd.Timestamp | None = None,
#         *,
#         duration: int | None = None,
#         hfreq: int | None = None,
#         limit: int = 1500,
#         fields: list[LiveFeedField] = [
#             "flight",
#             "reg",
#             "route",
#             "type",
#         ],
#     ) -> LiveFeedAPIResp:
#         """
#         Fetch live feed data.

#         *Related: [fr24.grpc.live_feed_world_data][]*

#         :param timestamp: Unix timestamp (seconds) of the live feed data.
#             If `None`, the latest live data will be fetched. Otherwise,
#             historical data will be fetched instead.
#         :param duration: Prefetch duration (default: `7` seconds). Should only
#             be set for historical data.
#         :param hfreq: High frequency mode (default: `0`). Should only be set
#             for historical data.
#         :param limit: Max number of flights (default 1500 for unauthenticated
#             users, 2000 for authenticated users)
#         :param fields: fields to include - for unauthenticated users, max 4
#             fields. When authenticated, `squawk`, `vspeed`, `airspace`,
#             `logo_id` and `age` can be included
#         """
#         ctx = self._construct_ctx(timestamp, duration, hfreq, limit, fields)
#         return LiveFeedAPIResp(ctx, await self._api._fetch(ctx))

#     def load(
#         self,
#         timestamp: int | str | datetime | pd.Timestamp,
#     ) -> LiveFeedArrow:
#         """
#         Get live feed data from the
#         [cache](../usage/cli.md#directories). If the file does not exist,
#         an empty table will be returned.

#         :param timestamp: Unix timestamp (seconds) of the saved feed snapshot.
#         """
#         ctx = self._construct_ctx(timestamp, None, None, None, None)
#         return LiveFeedArrow.from_cache(ctx)

#     def _construct_ctx(
#         self,
#         timestamp: int | str | datetime | pd.Timestamp | None,
#         duration: int | None,
#         hfreq: int | None,
#         limit: int | None,
#         fields: list[LiveFeedField] | None,
#     ) -> LiveFeedContext:
#         ts = to_unix_timestamp(timestamp)
#         if ts is None and (hfreq is not None or duration is not None):
#             raise ValueError(
#                 "`hfreq` and `duration` can only be set for historical data."
#             )
#         return {
#             "timestamp": ts,
#             "source": "live" if ts is None else "playback",
#             "duration": duration,
#             "hfreq": hfreq,
#             "limit": limit,
#             "fields": fields,
#             "base_dir": self._base_dir,
#         }
