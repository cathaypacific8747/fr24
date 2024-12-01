from fr24.proto import _common_pb2 as __common_pb2
from fr24.proto import _live_feed_pb2 as __live_feed_pb2
from fr24.proto import _health_pb2 as __health_pb2
from fr24.proto import _nearest_flights_pb2 as __nearest_flights_pb2
from fr24.proto import _live_flight_status_pb2 as __live_flight_status_pb2
from fr24.proto import _fetch_search_index_pb2 as __fetch_search_index_pb2
from fr24.proto import _follow_flight_pb2 as __follow_flight_pb2
from fr24.proto import _top_flights_pb2 as __top_flights_pb2
from fr24.proto import _live_trail_pb2 as __live_trail_pb2
from fr24.proto import _historic_trail_pb2 as __historic_trail_pb2
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar
from fr24.proto._common_pb2 import EMSInfo as EMSInfo
from fr24.proto._common_pb2 import EMSAvailability as EMSAvailability
from fr24.proto._common_pb2 import Schedule as Schedule
from fr24.proto._common_pb2 import Route as Route
from fr24.proto._common_pb2 import ExtraFlightInfo as ExtraFlightInfo
from fr24.proto._common_pb2 import SourceStats as SourceStats
from fr24.proto._common_pb2 import Stats as Stats
from fr24.proto._common_pb2 import RecentPosition as RecentPosition
from fr24.proto._common_pb2 import PositionBuffer as PositionBuffer
from fr24.proto._common_pb2 import Flight as Flight
from fr24.proto._common_pb2 import Duration as Duration
from fr24.proto._common_pb2 import Tick as Tick
from fr24.proto._common_pb2 import RadarHistoryRecord as RadarHistoryRecord
from fr24.proto._common_pb2 import RestrictionVisibility as RestrictionVisibility
from fr24.proto._common_pb2 import Service as Service
from fr24.proto._common_pb2 import TrafficType as TrafficType
from fr24.proto._common_pb2 import DataSource as DataSource
from fr24.proto._common_pb2 import Icon as Icon
from fr24.proto._common_pb2 import Status as Status
from fr24.proto._common_pb2 import EmergencyStatus as EmergencyStatus
from fr24.proto._live_feed_pb2 import LocationBoundaries as LocationBoundaries
from fr24.proto._live_feed_pb2 import VisibilitySettings as VisibilitySettings
from fr24.proto._live_feed_pb2 import AirportFilter as AirportFilter
from fr24.proto._live_feed_pb2 import Interval as Interval
from fr24.proto._live_feed_pb2 import AirlineFilter as AirlineFilter
from fr24.proto._live_feed_pb2 import Filter as Filter
from fr24.proto._live_feed_pb2 import LiveFeedRequest as LiveFeedRequest
from fr24.proto._live_feed_pb2 import LiveFeedResponse as LiveFeedResponse
from fr24.proto._live_feed_pb2 import PlaybackRequest as PlaybackRequest
from fr24.proto._live_feed_pb2 import PlaybackResponse as PlaybackResponse
from fr24.proto._live_feed_pb2 import AirportFilterType as AirportFilterType
from fr24.proto._live_feed_pb2 import AirlineFilterType as AirlineFilterType
from fr24.proto._health_pb2 import Ping as Ping
from fr24.proto._health_pb2 import Pong as Pong
from fr24.proto._nearest_flights_pb2 import Geolocation as Geolocation
from fr24.proto._nearest_flights_pb2 import NearestFlightsRequest as NearestFlightsRequest
from fr24.proto._nearest_flights_pb2 import NearbyFlight as NearbyFlight
from fr24.proto._nearest_flights_pb2 import NearestFlightsResponse as NearestFlightsResponse
from fr24.proto._live_flight_status_pb2 import LiveFlightStatusData as LiveFlightStatusData
from fr24.proto._live_flight_status_pb2 import LiveFlightsStatusRequest as LiveFlightsStatusRequest
from fr24.proto._live_flight_status_pb2 import _Unknown as _Unknown
from fr24.proto._live_flight_status_pb2 import LiveFlightsStatusResponse as LiveFlightsStatusResponse
from fr24.proto._fetch_search_index_pb2 import FlightSearchData as FlightSearchData
from fr24.proto._fetch_search_index_pb2 import FetchSearchIndexRequest as FetchSearchIndexRequest
from fr24.proto._fetch_search_index_pb2 import FetchSearchIndexResponse as FetchSearchIndexResponse
from fr24.proto._follow_flight_pb2 import ImageInfo as ImageInfo
from fr24.proto._follow_flight_pb2 import AircraftInfo as AircraftInfo
from fr24.proto._follow_flight_pb2 import Point as Point
from fr24.proto._follow_flight_pb2 import Coordinate as Coordinate
from fr24.proto._follow_flight_pb2 import Fix as Fix
from fr24.proto._follow_flight_pb2 import AltArrival as AltArrival
from fr24.proto._follow_flight_pb2 import FlightPlan as FlightPlan
from fr24.proto._follow_flight_pb2 import ScheduleInfo as ScheduleInfo
from fr24.proto._follow_flight_pb2 import FlightProgress as FlightProgress
from fr24.proto._follow_flight_pb2 import FollowFlightRequest as FollowFlightRequest
from fr24.proto._follow_flight_pb2 import ExtendedFlightInfo as ExtendedFlightInfo
from fr24.proto._follow_flight_pb2 import TrailPoint as TrailPoint
from fr24.proto._follow_flight_pb2 import FollowFlightResponse as FollowFlightResponse
from fr24.proto._follow_flight_pb2 import FlightStage as FlightStage
from fr24.proto._follow_flight_pb2 import DelayStatus as DelayStatus
from fr24.proto._top_flights_pb2 import FollowedFlight as FollowedFlight
from fr24.proto._top_flights_pb2 import TopFlightsRequest as TopFlightsRequest
from fr24.proto._top_flights_pb2 import TopFlightsResponse as TopFlightsResponse
from fr24.proto._live_trail_pb2 import LiveTrailRequest as LiveTrailRequest
from fr24.proto._live_trail_pb2 import LiveTrailResponse as LiveTrailResponse
from fr24.proto._historic_trail_pb2 import HistoricTrailRequest as HistoricTrailRequest
from fr24.proto._historic_trail_pb2 import HistoricTrailResponse as HistoricTrailResponse

DESCRIPTOR: _descriptor.FileDescriptor
NOT_VISIBLE: __common_pb2.RestrictionVisibility
PARTIALLY_VISIBLE: __common_pb2.RestrictionVisibility
FULLY_VISIBLE: __common_pb2.RestrictionVisibility
PASSENGER: __common_pb2.Service
CARGO: __common_pb2.Service
MILITARY_AND_GOVERNMENT: __common_pb2.Service
BUSINESS_JETS: __common_pb2.Service
GENERAL_AVIATION: __common_pb2.Service
HELICOPTERS: __common_pb2.Service
LIGHTER_THAN_AIR: __common_pb2.Service
GLIDERS: __common_pb2.Service
DRONES: __common_pb2.Service
GROUND_VEHICLES: __common_pb2.Service
OTHER_SERVICE: __common_pb2.Service
NON_CATEGORIZED: __common_pb2.Service
NONE: __common_pb2.TrafficType
GROUND_ONLY: __common_pb2.TrafficType
AIRBORNE_ONLY: __common_pb2.TrafficType
ALL: __common_pb2.TrafficType
ADSB: __common_pb2.DataSource
MLAT: __common_pb2.DataSource
FLARM: __common_pb2.DataSource
FAA: __common_pb2.DataSource
ESTIMATED: __common_pb2.DataSource
SATELLITE: __common_pb2.DataSource
OTHER_DATA_SOURCE: __common_pb2.DataSource
UAT: __common_pb2.DataSource
SPIDERTRACKS: __common_pb2.DataSource
AUS: __common_pb2.DataSource
B738: __common_pb2.Icon
FGTR: __common_pb2.Icon
ASW20: __common_pb2.Icon
C206: __common_pb2.Icon
C303: __common_pb2.Icon
LJ60: __common_pb2.Icon
Q300: __common_pb2.Icon
B736: __common_pb2.Icon
FOKKER100: __common_pb2.Icon
RJ85: __common_pb2.Icon
A320: __common_pb2.Icon
B757: __common_pb2.Icon
B767: __common_pb2.Icon
A3ST: __common_pb2.Icon
MD11: __common_pb2.Icon
A330: __common_pb2.Icon
A343: __common_pb2.Icon
A346: __common_pb2.Icon
B777: __common_pb2.Icon
B747: __common_pb2.Icon
A380: __common_pb2.Icon
A225: __common_pb2.Icon
SI2: __common_pb2.Icon
EC: __common_pb2.Icon
BALL: __common_pb2.Icon
GRND: __common_pb2.Icon
SLEI: __common_pb2.Icon
DRON: __common_pb2.Icon
SAT: __common_pb2.Icon
ISS: __common_pb2.Icon
NORMAL: __common_pb2.Status
BACKGROUND: __common_pb2.Status
EMERGENCY: __common_pb2.Status
NOT_AVAILABLE: __common_pb2.Status
LIVE: __common_pb2.Status
NO_EMERGENCY: __common_pb2.EmergencyStatus
GENERAL_EMERGENCY: __common_pb2.EmergencyStatus
LIFEGUARD_MEDICAL_EMERGENCY: __common_pb2.EmergencyStatus
MINIMUM_FUEL: __common_pb2.EmergencyStatus
NO_COMMUNICATIONS: __common_pb2.EmergencyStatus
UNLAWFUL_INTERFERENCE: __common_pb2.EmergencyStatus
DOWNED_AIRCRAFT: __common_pb2.EmergencyStatus
RESERVED: __common_pb2.EmergencyStatus
BOTH: __live_feed_pb2.AirportFilterType
INBOUND: __live_feed_pb2.AirportFilterType
OUTBOUND: __live_feed_pb2.AirportFilterType
PAINTED_AS: __live_feed_pb2.AirlineFilterType
OPERATED_AS: __live_feed_pb2.AirlineFilterType
UNKNOWN: __follow_flight_pb2.FlightStage
ON_GROUND: __follow_flight_pb2.FlightStage
ASCENDING: __follow_flight_pb2.FlightStage
AIRBORNE: __follow_flight_pb2.FlightStage
DESCENDING: __follow_flight_pb2.FlightStage
DIVERSION: __follow_flight_pb2.FlightStage
GRAY: __follow_flight_pb2.DelayStatus
GREEN: __follow_flight_pb2.DelayStatus
YELLOW: __follow_flight_pb2.DelayStatus
RED: __follow_flight_pb2.DelayStatus
