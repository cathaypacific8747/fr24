from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Generic, Protocol, TypeVar, Union

from google.protobuf.json_format import MessageToDict
from typing_extensions import runtime_checkable

from .cache import FR24Cache
from .grpc import (
    LiveFeedParams,
    LiveFeedPlaybackParams,
    NearestFlightsParams,
    live_feed,
    live_feed_df,
    live_feed_playback,
    live_feed_playback_df,
    nearest_flights,
    nearest_flights_df,
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
from .proto import SupportsToProto, parse_data
from .proto.v1_pb2 import (
    LiveFeedResponse,
    NearestFlightsResponse,
    PlaybackResponse,
)
from .types import overwrite_args_signature_from
from .types.flight_list import FLIGHT_LIST_EMPTY, FlightList
from .types.playback import Playback
from .utils import (
    SupportsToDict,
    SupportsToPolars,
    get_current_timestamp,
    parse_server_timestamp,
    write_table,
)

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any, AsyncIterator

    import httpx
    import polars as pl
    from typing_extensions import TypeAlias

    from . import HTTPClient
    from .cache import FR24Cache
    from .utils import SupportedFormats

_log = logging.getLogger(__name__)

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

    def build_nearest_flights(self) -> NearestFlightsService:
        return NearestFlightsService(self)


RequestT = TypeVar("RequestT")
"""Arguments for the request"""


@runtime_checkable
class SupportsFetch(Protocol[RequestT]):
    async def fetch(self, *args: Any, **kwargs: Any) -> APIResult[RequestT]:
        """Fetches data from the API."""


@dataclass
class APIResult(Generic[RequestT]):
    """
    Wraps the raw `Response` with request context.

    Note that at this stage, the response holds the *raw* bytes, possibly
    encoded with a scheme. Retrieve the raw bytes with `response.content` or
    parse it into json with `response.json()`.
    """

    request: RequestT
    response: httpx.Response


WriteLocation: TypeAlias = Union[str, Path, IO[bytes], FR24Cache]


@runtime_checkable
class SupportsWriteTable(Protocol):
    def write_table(self, file: WriteLocation) -> None:
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
        See [fr24.json.FlightListParams][] for the detailed signature.
        """
        request = FlightListParams(*args, **kwargs)
        response = await flight_list(
            self.__factory.http.client,
            request,
            self.__factory.http.auth,
        )
        return FlightListResult(
            request=request,
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
        """
        Create an empty list of flight list API results.

        Methods `to_dict` and `to_polars` can be used collect all unique rows in
        each flight list.
        """
        return FlightListResultCollection()


@dataclass
class FlightListResult(
    APIResult[FlightListParams],
    SupportsToDict[FlightList],
    SupportsToPolars,
    SupportsWriteTable,
):
    """A single result from the flight list API."""

    def to_dict(self) -> FlightList:
        return flight_list_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return flight_list_df(self.to_dict())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.flight_list(self.request.kind).new_bare_path(
                self.request.ident.upper()
            )
        write_table(self, file, format=format)


class FlightListResultCollection(
    list[FlightListResult],
    SupportsToDict[FlightList],
    SupportsToPolars,
    SupportsWriteTable,
):
    """A list of results from the flight list API."""

    def to_dict(self) -> FlightList:
        """
        Collects the raw bytes in each response into a single result.
        Duplicates are identified by their (flight id, time of departure),
        and are removed.

        No checking is made for the homogenity of the request parameters.
        """

        if len(self) == 0:
            return FLIGHT_LIST_EMPTY

        ident_hashes: set[int] = set()
        data = self[0].to_dict()
        flights_all = []
        for result in self:
            if (
                flights := result.to_dict()["result"]["response"]["data"]
            ) is None:
                continue
            for flight in flights:
                # NOTE: for future scheduled flights:
                # - the flight id is empty
                # - the standard time of departure is most certainly known
                # -> we use the STOD as the primary key for duplicates
                flight_id = flight["identification"]["id"]
                stod = flight["time"]["scheduled"]["departure"]
                ident_hash = hash((flight_id, stod))
                if ident_hash in ident_hashes:
                    if stod is not None:
                        _log.info(
                            f"skipping duplicate: {flight_id=} and {stod=}"
                        )
                        continue
                    else:
                        # changed from assert to avoid hard error
                        _log.warning(f"unexpected empty STOD for {flight_id=}")
                ident_hashes.add(ident_hash)
                flights_all.append(flight)

        data["result"]["response"]["data"] = flights_all
        return data

    def to_polars(self) -> pl.DataFrame:
        return flight_list_df(self.to_dict())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if not self:
            raise ValueError(
                "cannot save an empty flight list, "
                "must contain at least one valid flight list response"
            )
        if isinstance(file, FR24Cache):
            file = file.flight_list(self[0].request.kind).new_bare_path(
                self[0].request.ident.upper()
            )
        write_table(self, file, format=format)


@dataclass(frozen=True)
class PlaybackService(SupportsFetch[PlaybackParams]):
    """Playback service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(PlaybackParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> PlaybackResult:
        """See [fr24.json.PlaybackParams][] for the detailed signature."""
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
    SupportsWriteTable,
):
    def to_dict(self) -> Playback:
        return playback_parse(self.response)

    def to_polars(self) -> pl.DataFrame:
        return playback_df(self.to_dict())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.playback.new_bare_path(
                str(self.request.flight_id).upper()
            )
        write_table(self, file, format=format)


#
# gRPC
#


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
        timestamp = parse_server_timestamp(response) or get_current_timestamp()
        return LiveFeedResult(
            request=LiveFeedParams(*args, **kwargs),
            response=response,
            timestamp=timestamp,
        )


@dataclass
class LiveFeedResult(
    APIResult[LiveFeedParams],
    SupportsToProto[LiveFeedResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    timestamp: int

    def to_proto(self) -> LiveFeedResponse:
        return parse_data(self.response.content, LiveFeedResponse).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return live_feed_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.live_feed.new_bare_path(str(self.timestamp))
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
    SupportsWriteTable,
):
    def to_proto(self) -> PlaybackResponse:
        return parse_data(self.response.content, PlaybackResponse).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return live_feed_playback_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.live_feed.new_bare_path(str(self.request.timestamp))
        write_table(self, file, format=format)


@dataclass(frozen=True)
class NearestFlightsService(SupportsFetch[NearestFlightsParams]):
    """Nearest flights service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(NearestFlightsParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> NearestFlightsResult:
        """Fetch the nearest flights.
        See [fr24.grpc.NearestFlightsParams][] for the detailed signature.
        """
        request = NearestFlightsParams(*args, **kwargs)
        response = await nearest_flights(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        )
        timestamp = parse_server_timestamp(response) or get_current_timestamp()
        return NearestFlightsResult(
            request=request,
            response=response,
            timestamp=timestamp,
        )


@dataclass
class NearestFlightsResult(
    APIResult[NearestFlightsParams],
    SupportsToProto[NearestFlightsResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    timestamp: int

    def to_proto(self) -> NearestFlightsResponse:
        return parse_data(
            self.response.content, NearestFlightsResponse
        ).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return nearest_flights_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            lon6 = int(self.request.lon * 1e6)
            lat6 = int(self.request.lat * 1e6)
            file = file.nearest_flights.new_bare_path(
                f"{lon6}_{lat6}_{self.timestamp}"
            )
        write_table(self, file, format=format)
