from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    Generic,
    Protocol,
    TypeVar,
    Union,
)

from google.protobuf.json_format import MessageToDict
from typing_extensions import runtime_checkable

from .cache import FR24Cache
from .grpc import (
    FlightDetailsParams,
    FollowFlightParams,
    LiveFeedParams,
    LiveFeedPlaybackParams,
    LiveFlightsStatusParams,
    NearestFlightsParams,
    PlaybackFlightParams,
    TopFlightsParams,
    flight_details,
    flight_details_df,
    follow_flight_stream,
    live_feed,
    live_feed_df,
    live_feed_playback,
    live_feed_playback_df,
    live_flights_status,
    live_flights_status_df,
    nearest_flights,
    nearest_flights_df,
    playback_flight,
    playback_flight_df,
    top_flights,
    top_flights_df,
)
from .json import (
    AirportListParams,
    FindParams,
    FlightListParams,
    PlaybackParams,
    airport_list,
    airport_list_parse,
    find,
    find_parse,
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
    FlightDetailsResponse,
    FollowFlightResponse,
    LiveFeedResponse,
    LiveFlightsStatusResponse,
    NearestFlightsResponse,
    PlaybackFlightResponse,
    PlaybackResponse,
    TopFlightsResponse,
)
from .types import overwrite_args_signature_from
from .types.json import (
    FLIGHT_LIST_EMPTY,
    AirportList,
    Find,
    FlightList,
    Playback,
)
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

    def build_airport_list(self) -> AirportListService:
        return AirportListService(self)

    def build_find(self) -> FindService:
        return FindService(self)

    def build_nearest_flights(self) -> NearestFlightsService:
        return NearestFlightsService(self)

    def build_live_flights_status(self) -> LiveFlightsStatusService:
        return LiveFlightsStatusService(self)

    def build_flight_details(self) -> FlightDetailsService:
        return FlightDetailsService(self)

    def build_top_flights(self) -> TopFlightsService:
        return TopFlightsService(self)

    def build_follow_flight(self) -> FollowFlightService:
        return FollowFlightService(self)

    def build_playback_flight(self) -> PlaybackFlightService:
        return PlaybackFlightService(self)


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
        params = FlightListParams(*args, **kwargs)
        response = await flight_list(
            self.__factory.http.client,
            params,
            self.__factory.http.auth,
        )
        return FlightListResult(
            request=params,
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
            file = file.flight_list(self.request.kind).get_path(
                self.request.ident
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
            file = file.flight_list(self[0].request.kind).get_path(
                self[0].request.ident
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
            request=params,
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
            file = file.playback.get_path(self.request.flight_id)
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
            file = file.live_feed.get_path(self.timestamp)
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
            file = file.live_feed.get_path(self.request.timestamp)
        write_table(self, file, format=format)


@dataclass(frozen=True)
class AirportListService(SupportsFetch[AirportListParams]):
    """Airport list service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(AirportListParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> AirportListResult:
        """Fetch the airport list.
        See [fr24.json.AirportListParams][] for the detailed signature.
        """
        params = AirportListParams(*args, **kwargs)
        response = await airport_list(
            self.__factory.http.client,
            params,
            self.__factory.http.auth,
        )
        return AirportListResult(
            request=params,
            response=response,
        )


@dataclass
class AirportListResult(
    APIResult[AirportListParams],
    SupportsToDict[AirportList],
):
    def to_dict(self) -> AirportList:
        """Parse the response into a dictionary."""
        return airport_list_parse(self.response)


@dataclass(frozen=True)
class FindService(SupportsFetch[FindParams]):
    """Find service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(FindParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> FindResult:
        """Fetch the find results.
        See [fr24.json.FindParams][] for the detailed signature.
        """
        params = FindParams(*args, **kwargs)
        response = await find(
            self.__factory.http.client,
            params,
            self.__factory.http.auth,
        )
        return FindResult(
            request=params,
            response=response,
        )


@dataclass
class FindResult(
    APIResult[FindParams],
    SupportsToDict[Find],
):
    """A single result from the find API."""

    def to_dict(self) -> Find:
        """Parse the response into a dictionary."""
        return find_parse(self.response)


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
            file = file.nearest_flights.get_path(
                self.request.lat, self.request.lon, self.timestamp
            )
        write_table(self, file, format=format)


@dataclass(frozen=True)
class LiveFlightsStatusService(SupportsFetch[LiveFlightsStatusParams]):
    """Live flights status service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(LiveFlightsStatusParams)
    async def fetch(
        self, /, *args: Any, **kwargs: Any
    ) -> LiveFlightsStatusResult:
        """Fetch the live flights status.
        See [fr24.grpc.LiveFlightsStatusParams][] for the detailed signature.
        """
        request = LiveFlightsStatusParams(*args, **kwargs)
        response = await live_flights_status(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        )
        timestamp = parse_server_timestamp(response) or get_current_timestamp()
        return LiveFlightsStatusResult(
            request=request,
            response=response,
            timestamp=timestamp,
        )


@dataclass
class LiveFlightsStatusResult(
    APIResult[LiveFlightsStatusParams],
    SupportsToProto[LiveFlightsStatusResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    timestamp: int

    def to_proto(self) -> LiveFlightsStatusResponse:
        return parse_data(
            self.response.content, LiveFlightsStatusResponse
        ).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return live_flights_status_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.live_flights_status.get_path(self.timestamp)
        write_table(self, file, format=format)


@dataclass(frozen=True)
class FollowFlightService:
    """Follow flight service for real-time streaming."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(FollowFlightParams)
    async def stream(
        self, /, *args: Any, **kwargs: Any
    ) -> AsyncGenerator[FollowFlightResult, None]:
        """Stream real-time updates for a flight.
        See [fr24.grpc.FollowFlightParams][] for the detailed signature.
        """
        request = FollowFlightParams(*args, **kwargs)
        async for response in follow_flight_stream(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        ):
            yield FollowFlightResult(
                request=request,
                response=response,
            )


@dataclass
class FollowFlightResult(
    SupportsToProto[FollowFlightResponse],
    SupportsToDict[dict[str, Any]],
):
    request: FollowFlightParams
    response: bytes

    def to_proto(self) -> FollowFlightResponse:
        return parse_data(self.response, FollowFlightResponse).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)


@dataclass(frozen=True)
class TopFlightsService(SupportsFetch[TopFlightsParams]):
    """Top flights service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(TopFlightsParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> TopFlightsResult:
        """Fetch the top flights.
        See [fr24.grpc.TopFlightsParams][] for the detailed signature.
        """
        request = TopFlightsParams(*args, **kwargs)
        response = await top_flights(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        )
        timestamp = parse_server_timestamp(response) or get_current_timestamp()
        return TopFlightsResult(
            request=request,
            response=response,
            timestamp=timestamp,
        )


@dataclass
class TopFlightsResult(
    APIResult[TopFlightsParams],
    SupportsToProto[TopFlightsResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    timestamp: int

    def to_proto(self) -> TopFlightsResponse:
        return parse_data(self.response.content, TopFlightsResponse).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return top_flights_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.top_flights.get_path(self.timestamp)
        write_table(self, file, format=format)


@dataclass(frozen=True)
class FlightDetailsService(SupportsFetch[FlightDetailsParams]):
    """Flight details service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(FlightDetailsParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> FlightDetailsResult:
        """Fetch flight details.
        See [fr24.grpc.FlightDetailsParams][] for the detailed signature.
        """
        request = FlightDetailsParams(*args, **kwargs)
        response = await flight_details(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        )
        timestamp = parse_server_timestamp(response) or get_current_timestamp()
        return FlightDetailsResult(
            request=request,
            response=response,
            timestamp=timestamp,
        )


@dataclass
class FlightDetailsResult(
    APIResult[FlightDetailsParams],
    SupportsToProto[FlightDetailsResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    timestamp: int

    def to_proto(self) -> FlightDetailsResponse:
        return parse_data(self.response.content, FlightDetailsResponse).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return flight_details_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.flight_details.get_path(
                self.request.flight_id, self.timestamp
            )
        write_table(self, file, format=format)


@dataclass(frozen=True)
class PlaybackFlightService(SupportsFetch[PlaybackFlightParams]):
    """Playback flight service."""

    __factory: ServiceFactory

    @overwrite_args_signature_from(PlaybackFlightParams)
    async def fetch(self, /, *args: Any, **kwargs: Any) -> PlaybackFlightResult:
        """Fetch playback flight details.
        See [fr24.grpc.PlaybackFlightParams][] for the detailed signature.
        """
        request = PlaybackFlightParams(*args, **kwargs)
        response = await playback_flight(
            self.__factory.http.client,
            request.to_proto(),
            self.__factory.http.auth,
        )
        return PlaybackFlightResult(
            request=request,
            response=response,
        )


@dataclass
class PlaybackFlightResult(
    APIResult[PlaybackFlightParams],
    SupportsToProto[PlaybackFlightResponse],
    SupportsToDict[dict[str, Any]],
    SupportsToPolars,
    SupportsWriteTable,
):
    def to_proto(self) -> PlaybackFlightResponse:
        return parse_data(
            self.response.content, PlaybackFlightResponse
        ).unwrap()

    def to_dict(self) -> dict[str, Any]:
        return MessageToDict(self.to_proto(), preserving_proto_field_name=True)

    def to_polars(self) -> pl.DataFrame:
        return playback_flight_df(self.to_proto())

    def write_table(
        self,
        file: WriteLocation,
        *,
        format: SupportedFormats = "parquet",
    ) -> None:
        if isinstance(file, FR24Cache):
            file = file.playback_flight.get_path(
                self.request.flight_id, self.request.timestamp
            )
        write_table(self, file, format=format)
