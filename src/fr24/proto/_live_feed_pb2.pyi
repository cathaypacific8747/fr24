from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AirportFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOTH: _ClassVar[AirportFilterType]
    INBOUND: _ClassVar[AirportFilterType]
    OUTBOUND: _ClassVar[AirportFilterType]

class AirlineFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAINTED_AS: _ClassVar[AirlineFilterType]
    OPERATED_AS: _ClassVar[AirlineFilterType]
BOTH: AirportFilterType
INBOUND: AirportFilterType
OUTBOUND: AirportFilterType
PAINTED_AS: AirlineFilterType
OPERATED_AS: AirlineFilterType

class LocationBoundaries(_message.Message):
    __slots__ = ("north", "south", "west", "east")
    NORTH_FIELD_NUMBER: _ClassVar[int]
    SOUTH_FIELD_NUMBER: _ClassVar[int]
    WEST_FIELD_NUMBER: _ClassVar[int]
    EAST_FIELD_NUMBER: _ClassVar[int]
    north: float
    south: float
    west: float
    east: float
    def __init__(self, north: _Optional[float] = ..., south: _Optional[float] = ..., west: _Optional[float] = ..., east: _Optional[float] = ...) -> None: ...

class VisibilitySettings(_message.Message):
    __slots__ = ("sources_list", "services_list", "traffic_type", "only_restricted")
    SOURCES_LIST_FIELD_NUMBER: _ClassVar[int]
    SERVICES_LIST_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    ONLY_RESTRICTED_FIELD_NUMBER: _ClassVar[int]
    sources_list: _containers.RepeatedScalarFieldContainer[__common_pb2.DataSource]
    services_list: _containers.RepeatedScalarFieldContainer[__common_pb2.Service]
    traffic_type: __common_pb2.TrafficType
    only_restricted: bool
    def __init__(self, sources_list: _Optional[_Iterable[_Union[__common_pb2.DataSource, str]]] = ..., services_list: _Optional[_Iterable[_Union[__common_pb2.Service, str]]] = ..., traffic_type: _Optional[_Union[__common_pb2.TrafficType, str]] = ..., only_restricted: bool = ...) -> None: ...

class AirportFilter(_message.Message):
    __slots__ = ("iata", "country_id", "type")
    IATA_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    iata: str
    country_id: int
    type: AirportFilterType
    def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ..., type: _Optional[_Union[AirportFilterType, str]] = ...) -> None: ...

class Interval(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class AirlineFilter(_message.Message):
    __slots__ = ("icao", "type")
    ICAO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    icao: str
    type: AirlineFilterType
    def __init__(self, icao: _Optional[str] = ..., type: _Optional[_Union[AirlineFilterType, str]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("altitude_ranges_list", "speed_ranges_list", "airlines_list", "callsigns_list", "radars_list", "regs_list", "airports_list", "flights_list", "types_list", "birth_year_ranges_list", "squawks_list", "origins_list", "destinations_list", "categories_list", "airspaces_list")
    ALTITUDE_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    SPEED_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRLINES_LIST_FIELD_NUMBER: _ClassVar[int]
    CALLSIGNS_LIST_FIELD_NUMBER: _ClassVar[int]
    RADARS_LIST_FIELD_NUMBER: _ClassVar[int]
    REGS_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRPORTS_LIST_FIELD_NUMBER: _ClassVar[int]
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    TYPES_LIST_FIELD_NUMBER: _ClassVar[int]
    BIRTH_YEAR_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    SQUAWKS_LIST_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_LIST_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRSPACES_LIST_FIELD_NUMBER: _ClassVar[int]
    altitude_ranges_list: _containers.RepeatedCompositeFieldContainer[Interval]
    speed_ranges_list: _containers.RepeatedCompositeFieldContainer[Interval]
    airlines_list: _containers.RepeatedCompositeFieldContainer[AirlineFilter]
    callsigns_list: _containers.RepeatedScalarFieldContainer[str]
    radars_list: _containers.RepeatedScalarFieldContainer[str]
    regs_list: _containers.RepeatedScalarFieldContainer[str]
    airports_list: _containers.RepeatedCompositeFieldContainer[AirportFilter]
    flights_list: _containers.RepeatedScalarFieldContainer[str]
    types_list: _containers.RepeatedScalarFieldContainer[str]
    birth_year_ranges_list: _containers.RepeatedCompositeFieldContainer[Interval]
    squawks_list: _containers.RepeatedScalarFieldContainer[int]
    origins_list: _containers.RepeatedCompositeFieldContainer[AirportFilter]
    destinations_list: _containers.RepeatedCompositeFieldContainer[AirportFilter]
    categories_list: _containers.RepeatedScalarFieldContainer[__common_pb2.Service]
    airspaces_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, altitude_ranges_list: _Optional[_Iterable[_Union[Interval, _Mapping]]] = ..., speed_ranges_list: _Optional[_Iterable[_Union[Interval, _Mapping]]] = ..., airlines_list: _Optional[_Iterable[_Union[AirlineFilter, _Mapping]]] = ..., callsigns_list: _Optional[_Iterable[str]] = ..., radars_list: _Optional[_Iterable[str]] = ..., regs_list: _Optional[_Iterable[str]] = ..., airports_list: _Optional[_Iterable[_Union[AirportFilter, _Mapping]]] = ..., flights_list: _Optional[_Iterable[str]] = ..., types_list: _Optional[_Iterable[str]] = ..., birth_year_ranges_list: _Optional[_Iterable[_Union[Interval, _Mapping]]] = ..., squawks_list: _Optional[_Iterable[int]] = ..., origins_list: _Optional[_Iterable[_Union[AirportFilter, _Mapping]]] = ..., destinations_list: _Optional[_Iterable[_Union[AirportFilter, _Mapping]]] = ..., categories_list: _Optional[_Iterable[_Union[__common_pb2.Service, str]]] = ..., airspaces_list: _Optional[_Iterable[str]] = ...) -> None: ...

class LiveFeedRequest(_message.Message):
    __slots__ = ("bounds", "settings", "filters_list", "fleets_list", "highlight_mode", "stats", "limit", "maxage", "restriction_mode", "field_mask", "selected_flight_ids_list")
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    FLEETS_LIST_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_MODE_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAXAGE_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_MODE_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHT_IDS_LIST_FIELD_NUMBER: _ClassVar[int]
    bounds: LocationBoundaries
    settings: VisibilitySettings
    filters_list: Filter
    fleets_list: str
    highlight_mode: bool
    stats: bool
    limit: int
    maxage: int
    restriction_mode: __common_pb2.RestrictionVisibility
    field_mask: _field_mask_pb2.FieldMask
    selected_flight_ids_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, bounds: _Optional[_Union[LocationBoundaries, _Mapping]] = ..., settings: _Optional[_Union[VisibilitySettings, _Mapping]] = ..., filters_list: _Optional[_Union[Filter, _Mapping]] = ..., fleets_list: _Optional[str] = ..., highlight_mode: bool = ..., stats: bool = ..., limit: _Optional[int] = ..., maxage: _Optional[int] = ..., restriction_mode: _Optional[_Union[__common_pb2.RestrictionVisibility, str]] = ..., field_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ..., selected_flight_ids_list: _Optional[_Iterable[int]] = ...) -> None: ...

class LiveFeedResponse(_message.Message):
    __slots__ = ("flights_list", "stats", "selected_flight_info")
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHT_INFO_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[__common_pb2.Flight]
    stats: __common_pb2.Stats
    selected_flight_info: _containers.RepeatedCompositeFieldContainer[__common_pb2.Flight]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[__common_pb2.Flight, _Mapping]]] = ..., stats: _Optional[_Union[__common_pb2.Stats, _Mapping]] = ..., selected_flight_info: _Optional[_Iterable[_Union[__common_pb2.Flight, _Mapping]]] = ...) -> None: ...

class PlaybackRequest(_message.Message):
    __slots__ = ("live_feed_request", "timestamp", "prefetch", "hfreq")
    LIVE_FEED_REQUEST_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PREFETCH_FIELD_NUMBER: _ClassVar[int]
    HFREQ_FIELD_NUMBER: _ClassVar[int]
    live_feed_request: LiveFeedRequest
    timestamp: int
    prefetch: int
    hfreq: int
    def __init__(self, live_feed_request: _Optional[_Union[LiveFeedRequest, _Mapping]] = ..., timestamp: _Optional[int] = ..., prefetch: _Optional[int] = ..., hfreq: _Optional[int] = ...) -> None: ...

class PlaybackResponse(_message.Message):
    __slots__ = ("live_feed_response",)
    LIVE_FEED_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    live_feed_response: LiveFeedResponse
    def __init__(self, live_feed_response: _Optional[_Union[LiveFeedResponse, _Mapping]] = ...) -> None: ...
