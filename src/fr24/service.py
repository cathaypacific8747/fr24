from __future__ import annotations

import asyncio
import email.utils
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeVar,
)

from google.protobuf.json_format import MessageToDict
from typing_extensions import runtime_checkable

from .utils import SupportsToDict, SupportsToPolars, SupportsToProto

if TYPE_CHECKING:
    from typing import IO, Any

    import httpx
    import polars as pl

    from .cache import Cache

from .grpc import (
    LiveFeedParams,
    LiveFeedPlaybackParams,
    live_feed,
    live_feed_df,
    live_feed_parse,
    live_feed_playback,
    live_feed_playback_df,
    live_feed_playback_parse,
)
from .json import (
    FlightListParams,
    PlaybackParams,
    flight_list,
    flight_list_df,
    flight_list_parse,
    playback,
    playback_df,
    playback_metadata_dict,
    playback_parse,
)
from .proto.v1_pb2 import LiveFeedResponse, PlaybackResponse
from .types import overwrite_args_signature_from
from .types.flight_list import FLIGHT_LIST_EMPTY, FlightList
from .types.playback import Playback
from .utils import BarePath, write_table

if TYPE_CHECKING:
    from pathlib import Path
    from typing import IO, AsyncIterator

    import polars as pl

    from . import HTTPClient
    from .cache import Cache
    from .utils import SupportedFormats


#
# important traits and dataclasses
#


@dataclass
class ServiceFactory:
    http: HTTPClient

    def build_flight_list(self) -> FlightListService:
        return FlightListService(self)

    def build_playback(self) -> PlaybackService:
        return PlaybackService(self)

    def build_live_feed(self) -> LiveFeedService:
        return LiveFeedService(self)

    def build_live_feed_playback(self) -> LiveFeedPlaybackService:
        return LiveFeedPlaybackService(self)


RequestT = TypeVar("RequestT")
"""Arguments for the request"""


@runtime_checkable
class SupportsFetch(Protocol[RequestT]):
    async def fetch(self, *args: Any, **kwargs: Any) -> APIResult[RequestT]:
        """Fetches data from the API."""


@dataclass
class APIResult(Generic[RequestT]):
    """Wraps raw bytes with context."""

    request: RequestT
    response: httpx.Response


@runtime_checkable
class SupportsWrite(Protocol):
    def write(self, file: Path | IO[bytes] | Cache) -> None:
        """Writes the object to the given file path."""


#
# definitions for services and results
#


@dataclass(frozen=True)
class FlightListService(SupportsFetch[FlightListParams]):
    """Flight list service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(FlightListParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> FlightListResult:
        """
        Fetch the flight list.
        See [fr24.json.FlightListRequest][] for the detailed signature.
        """
        request = FlightListParams(*args, **kwargs)
        response = await flight_list(
            self.__factory.http.client,
            request,
            self.__factory.http.auth,
        )
        return FlightListResult(
            request=FlightListParams(*args, **kwargs),
            response=response,
        )

    @dataclass
    class FetchAllArgs(FlightListParams):
        """Arguments for fetching all pages of the flight list."""

        delay: int = field(default=5)

    @overwrite_args_signature_from(FetchAllArgs)
    async def fetch_all(
        self, /, *args: Any, **kwargs: Any
    ) -> AsyncIterator[FlightListResult]:
        """
        Fetch all pages of the flight list.

        See [fr24.service.FlightListService.FetchAllArgs][] for the detailed
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

    def new_result_collection(self) -> FlightListResultCollection:
        """Create an empty list of flight list API results."""
        return FlightListResultCollection()


@dataclass
class FlightListResult(
    APIResult[FlightListParams],
    SupportsToDict[FlightList],
    SupportsToPolars,
    SupportsWrite,
):
    def to_dict(self) -> FlightList:
        return flight_list_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return flight_list_df(self.to_dict())

    def write(
        self,
        file: Path | IO[bytes] | Cache,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, Cache):
            file = BarePath(
                file._flight_list_path(self.request.kind)
                / self.request.ident.upper()
            )
        write_table(self, file, format=format)


@dataclass
class FlightListResultCollection(
    list[FlightListResult],
    SupportsToDict[FlightList],
    SupportsToPolars,
    SupportsWrite,
):
    """A list of results from the flight list API."""

    def to_dict(self) -> FlightList:
        """
        Collects the raw bytes in each response into a single result.
        Duplicates are identified by their flight ids and are removed. Flights
        without an assigned id are kept intact.

        No checking is made for the homogenity of the request parameters.
        """

        if len(self) == 0:
            return FLIGHT_LIST_EMPTY

        flight_ids_seen: set[str | None] = set()
        data = self[0].to_dict()
        flights_all = []
        for result in self:
            if (
                flights := result.to_dict()["result"]["response"]["data"]
            ) is None:
                continue
            for flight in flights:
                if (
                    flight_id := flight["identification"]["id"]
                ) is not None and flight_id in flight_ids_seen:
                    continue
                flight_ids_seen.add(flight_id)
                flights_all.append(flight)

        data["result"]["response"]["data"] = flights_all
        return data

    def to_polars(self) -> pl.DataFrame:
        return flight_list_df(self.to_dict())

    def write(
        self,
        file: Path | IO[bytes] | Cache,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if not self:
            raise ValueError(
                "cannot save an empty flight list, "
                "must contain at least one valid flight list response"
            )
        if isinstance(file, Cache):
            file = BarePath(
                file._flight_list_path(self[0].request.kind)
                / self[0].request.ident.upper()
            )
        write_table(self, file, format=format)


@dataclass(frozen=True)
class PlaybackService(SupportsFetch[PlaybackParams]):
    """Playback service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(PlaybackParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> PlaybackResult:
        """
        FIXME - add docs
        See [fr24.json.PlaybackRequest][] for the detailed signature.
        """
        params = PlaybackParams(*args, **kwargs)
        response = await playback(
            self.__factory.http.client,
            params,
            self.__factory.http.auth,
        )
        return PlaybackResult(
            request=PlaybackParams(*args, **kwargs),
            response=response,
        )

    @classmethod
    def metadata(cls, response_dict: Playback) -> dict[str, Any]:
        # TODO: reconsider if we really want this here
        return playback_metadata_dict(
            response_dict["result"]["response"]["data"]["flight"]
        )


@dataclass
class PlaybackResult(
    APIResult[PlaybackParams],
    SupportsToDict[Playback],
    SupportsToPolars,
    SupportsWrite,
):
    def to_dict(self) -> Playback:
        return playback_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return playback_df(self.to_dict())

    def write(
        self,
        file: Path | IO[bytes] | Cache,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, Cache):
            file = BarePath(file._playback_path() / str(self.request.flight_id))
        write_table(self, file, format=format)


@dataclass(frozen=True)
class LiveFeedService(SupportsFetch[LiveFeedParams]):
    """Live feed service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(LiveFeedParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> LiveFeedResult:
        """
        Fetch the live feed.
        See [fr24.grpc.LiveFeedParams][] for the detailed signature.
        """
        params = LiveFeedParams(*args, **kwargs)
        response = await live_feed(
            self.__factory.http.client,
            params.to_proto(),
            self.__factory.http.auth,
        )
        # NOTE: serverTimeMs in the protobuf response would be more accurate
        server_date: str = response.headers.get("date")
        timestamp = int(
            email.utils.parsedate_to_datetime(server_date).timestamp()
            if server_date is not None
            else time.time()
        )
        return LiveFeedResult(
            request=LiveFeedParams(*args, **kwargs),
            response=response,
            timestamp=timestamp,
        )


#
# gRPC
#


@dataclass
class LiveFeedResult(
    APIResult[LiveFeedParams],
    SupportsToProto[LiveFeedResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWrite,
):
    timestamp: int

    def to_proto(self) -> LiveFeedResponse:
        return live_feed_parse(self.response)

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto())

    def to_polars(self) -> pl.DataFrame:
        return live_feed_df(self.to_proto())

    def write(
        self,
        file: Path | IO[bytes] | Cache,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, Cache):
            file = BarePath(file._feed_path() / str(self.timestamp))
        write_table(self, file, format=format)


@dataclass(frozen=True)
class LiveFeedPlaybackService(SupportsFetch[LiveFeedPlaybackParams]):
    """Live feed service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(LiveFeedPlaybackParams)
    async def fetch(
        self, /, *args: Any, **kwargs: Any
    ) -> LiveFeedPlaybackResult:
        """
        Fetch a playback of the live feed.
        See [fr24.grpc.LiveFeedPlaybackParams][] for the detailed signature.
        """
        params = LiveFeedPlaybackParams(*args, **kwargs)
        response = await live_feed_playback(
            self.__factory.http.client,
            params.to_proto(),
            self.__factory.http.auth,
        )
        return LiveFeedPlaybackResult(
            request=LiveFeedPlaybackParams(*args, **kwargs),
            response=response,
        )


@dataclass
class LiveFeedPlaybackResult(
    APIResult[LiveFeedPlaybackParams],
    SupportsToProto[PlaybackResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWrite,
):
    def to_proto(self) -> PlaybackResponse:
        return live_feed_playback_parse(self.response)

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto())

    def to_polars(self) -> pl.DataFrame:
        return live_feed_playback_df(self.to_proto())

    def write(
        self,
        file: Path | IO[bytes] | Cache,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, Cache):
            file = BarePath(file._feed_path() / str(self.request.timestamp))
        write_table(self, file, format=format)
