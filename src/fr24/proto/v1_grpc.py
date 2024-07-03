# Generated by the Protocol Buffers compiler. DO NOT EDIT!
# source: fr24/proto/v1.proto
# plugin: grpclib.plugin.main
import abc
import typing

import grpclib.const
import grpclib.client
if typing.TYPE_CHECKING:
    import grpclib.server

import fr24.proto._common_pb2
import fr24.proto._live_feed_pb2
import fr24.proto._health_pb2
import fr24.proto._nearest_flights_pb2
import fr24.proto._live_flight_status_pb2
import fr24.proto._fetch_search_index_pb2
import fr24.proto._follow_flight_pb2
import fr24.proto._top_flights_pb2
import fr24.proto._live_trail_pb2
import fr24.proto.v1_pb2


class FeedBase(abc.ABC):

    @abc.abstractmethod
    async def Echo(self, stream: 'grpclib.server.Stream[fr24.proto._health_pb2.Ping, fr24.proto._health_pb2.Pong]') -> None:
        pass

    @abc.abstractmethod
    async def CountDown(self, stream: 'grpclib.server.Stream[fr24.proto._common_pb2.Duration, fr24.proto._common_pb2.Tick]') -> None:
        pass

    @abc.abstractmethod
    async def LiveFeed(self, stream: 'grpclib.server.Stream[fr24.proto._live_feed_pb2.LiveFeedRequest, fr24.proto._live_feed_pb2.LiveFeedResponse]') -> None:
        pass

    @abc.abstractmethod
    async def Playback(self, stream: 'grpclib.server.Stream[fr24.proto._live_feed_pb2.PlaybackRequest, fr24.proto._live_feed_pb2.PlaybackResponse]') -> None:
        pass

    @abc.abstractmethod
    async def NearestFlights(self, stream: 'grpclib.server.Stream[fr24.proto._nearest_flights_pb2.NearestFlightsRequest, fr24.proto._nearest_flights_pb2.NearestFlightsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LiveFlightsStatus(self, stream: 'grpclib.server.Stream[fr24.proto._live_flight_status_pb2.LiveFlightsStatusRequest, fr24.proto._live_flight_status_pb2.LiveFlightsStatusResponse]') -> None:
        pass

    @abc.abstractmethod
    async def FetchSearchIndex(self, stream: 'grpclib.server.Stream[fr24.proto._fetch_search_index_pb2.FetchSearchIndexRequest, fr24.proto._fetch_search_index_pb2.FetchSearchIndexResponse]') -> None:
        pass

    @abc.abstractmethod
    async def FollowFlight(self, stream: 'grpclib.server.Stream[fr24.proto._follow_flight_pb2.FollowFlightRequest, fr24.proto._follow_flight_pb2.FollowFlightResponse]') -> None:
        pass

    @abc.abstractmethod
    async def TopFlights(self, stream: 'grpclib.server.Stream[fr24.proto._top_flights_pb2.TopFlightsRequest, fr24.proto._top_flights_pb2.TopFlightsResponse]') -> None:
        pass

    @abc.abstractmethod
    async def LiveTrail(self, stream: 'grpclib.server.Stream[fr24.proto._live_trail_pb2.LiveTrailRequest, fr24.proto._live_trail_pb2.LiveTrailResponse]') -> None:
        pass

    def __mapping__(self) -> typing.Dict[str, grpclib.const.Handler]:
        return {
            '/fr24.feed.api.v1.Feed/Echo': grpclib.const.Handler(
                self.Echo,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._health_pb2.Ping,
                fr24.proto._health_pb2.Pong,
            ),
            '/fr24.feed.api.v1.Feed/CountDown': grpclib.const.Handler(
                self.CountDown,
                grpclib.const.Cardinality.UNARY_STREAM,
                fr24.proto._common_pb2.Duration,
                fr24.proto._common_pb2.Tick,
            ),
            '/fr24.feed.api.v1.Feed/LiveFeed': grpclib.const.Handler(
                self.LiveFeed,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._live_feed_pb2.LiveFeedRequest,
                fr24.proto._live_feed_pb2.LiveFeedResponse,
            ),
            '/fr24.feed.api.v1.Feed/Playback': grpclib.const.Handler(
                self.Playback,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._live_feed_pb2.PlaybackRequest,
                fr24.proto._live_feed_pb2.PlaybackResponse,
            ),
            '/fr24.feed.api.v1.Feed/NearestFlights': grpclib.const.Handler(
                self.NearestFlights,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._nearest_flights_pb2.NearestFlightsRequest,
                fr24.proto._nearest_flights_pb2.NearestFlightsResponse,
            ),
            '/fr24.feed.api.v1.Feed/LiveFlightsStatus': grpclib.const.Handler(
                self.LiveFlightsStatus,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._live_flight_status_pb2.LiveFlightsStatusRequest,
                fr24.proto._live_flight_status_pb2.LiveFlightsStatusResponse,
            ),
            '/fr24.feed.api.v1.Feed/FetchSearchIndex': grpclib.const.Handler(
                self.FetchSearchIndex,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._fetch_search_index_pb2.FetchSearchIndexRequest,
                fr24.proto._fetch_search_index_pb2.FetchSearchIndexResponse,
            ),
            '/fr24.feed.api.v1.Feed/FollowFlight': grpclib.const.Handler(
                self.FollowFlight,
                grpclib.const.Cardinality.UNARY_STREAM,
                fr24.proto._follow_flight_pb2.FollowFlightRequest,
                fr24.proto._follow_flight_pb2.FollowFlightResponse,
            ),
            '/fr24.feed.api.v1.Feed/TopFlights': grpclib.const.Handler(
                self.TopFlights,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._top_flights_pb2.TopFlightsRequest,
                fr24.proto._top_flights_pb2.TopFlightsResponse,
            ),
            '/fr24.feed.api.v1.Feed/LiveTrail': grpclib.const.Handler(
                self.LiveTrail,
                grpclib.const.Cardinality.UNARY_UNARY,
                fr24.proto._live_trail_pb2.LiveTrailRequest,
                fr24.proto._live_trail_pb2.LiveTrailResponse,
            ),
        }


class FeedStub:

    def __init__(self, channel: grpclib.client.Channel) -> None:
        self.Echo = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/Echo',
            fr24.proto._health_pb2.Ping,
            fr24.proto._health_pb2.Pong,
        )
        self.CountDown = grpclib.client.UnaryStreamMethod(
            channel,
            '/fr24.feed.api.v1.Feed/CountDown',
            fr24.proto._common_pb2.Duration,
            fr24.proto._common_pb2.Tick,
        )
        self.LiveFeed = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/LiveFeed',
            fr24.proto._live_feed_pb2.LiveFeedRequest,
            fr24.proto._live_feed_pb2.LiveFeedResponse,
        )
        self.Playback = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/Playback',
            fr24.proto._live_feed_pb2.PlaybackRequest,
            fr24.proto._live_feed_pb2.PlaybackResponse,
        )
        self.NearestFlights = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/NearestFlights',
            fr24.proto._nearest_flights_pb2.NearestFlightsRequest,
            fr24.proto._nearest_flights_pb2.NearestFlightsResponse,
        )
        self.LiveFlightsStatus = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/LiveFlightsStatus',
            fr24.proto._live_flight_status_pb2.LiveFlightsStatusRequest,
            fr24.proto._live_flight_status_pb2.LiveFlightsStatusResponse,
        )
        self.FetchSearchIndex = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/FetchSearchIndex',
            fr24.proto._fetch_search_index_pb2.FetchSearchIndexRequest,
            fr24.proto._fetch_search_index_pb2.FetchSearchIndexResponse,
        )
        self.FollowFlight = grpclib.client.UnaryStreamMethod(
            channel,
            '/fr24.feed.api.v1.Feed/FollowFlight',
            fr24.proto._follow_flight_pb2.FollowFlightRequest,
            fr24.proto._follow_flight_pb2.FollowFlightResponse,
        )
        self.TopFlights = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/TopFlights',
            fr24.proto._top_flights_pb2.TopFlightsRequest,
            fr24.proto._top_flights_pb2.TopFlightsResponse,
        )
        self.LiveTrail = grpclib.client.UnaryUnaryMethod(
            channel,
            '/fr24.feed.api.v1.Feed/LiveTrail',
            fr24.proto._live_trail_pb2.LiveTrailRequest,
            fr24.proto._live_trail_pb2.LiveTrailResponse,
        )