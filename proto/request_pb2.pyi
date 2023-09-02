from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Service(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    PASSENGER: _ClassVar[Service]
    CARGO: _ClassVar[Service]
    MILITARY_AND_GOVERNMENT: _ClassVar[Service]
    BUSINESS_JETS: _ClassVar[Service]
    GENERAL_AVIATION: _ClassVar[Service]
    HELICOPTERS: _ClassVar[Service]
    LIGHTER_THAN_AIR: _ClassVar[Service]
    GLIDERS: _ClassVar[Service]
    DRONES: _ClassVar[Service]
    GROUND_VEHICLES: _ClassVar[Service]
    OTHER_SERVICE: _ClassVar[Service]
    NON_CATEGORIZED: _ClassVar[Service]

class DataSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ADSB: _ClassVar[DataSource]
    MLAT: _ClassVar[DataSource]
    FLARM: _ClassVar[DataSource]
    FAA: _ClassVar[DataSource]
    ESTIMATED: _ClassVar[DataSource]
    SATELLITE: _ClassVar[DataSource]
    OTHER_DATA_SOURCE: _ClassVar[DataSource]
    UAT: _ClassVar[DataSource]
    SPIDERTRACKS: _ClassVar[DataSource]
    AUS: _ClassVar[DataSource]

class TrafficType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    NONE: _ClassVar[TrafficType]
    GROUND_ONLY: _ClassVar[TrafficType]
    AIRBORNE_ONLY: _ClassVar[TrafficType]
    ALL: _ClassVar[TrafficType]
PASSENGER: Service
CARGO: Service
MILITARY_AND_GOVERNMENT: Service
BUSINESS_JETS: Service
GENERAL_AVIATION: Service
HELICOPTERS: Service
LIGHTER_THAN_AIR: Service
GLIDERS: Service
DRONES: Service
GROUND_VEHICLES: Service
OTHER_SERVICE: Service
NON_CATEGORIZED: Service
ADSB: DataSource
MLAT: DataSource
FLARM: DataSource
FAA: DataSource
ESTIMATED: DataSource
SATELLITE: DataSource
OTHER_DATA_SOURCE: DataSource
UAT: DataSource
SPIDERTRACKS: DataSource
AUS: DataSource
NONE: TrafficType
GROUND_ONLY: TrafficType
AIRBORNE_ONLY: TrafficType
ALL: TrafficType

class Bounds(_message.Message):
    __slots__ = ["north", "south", "west", "east"]
    NORTH_FIELD_NUMBER: _ClassVar[int]
    SOUTH_FIELD_NUMBER: _ClassVar[int]
    WEST_FIELD_NUMBER: _ClassVar[int]
    EAST_FIELD_NUMBER: _ClassVar[int]
    north: float
    south: float
    west: float
    east: float
    def __init__(self, north: _Optional[float] = ..., south: _Optional[float] = ..., west: _Optional[float] = ..., east: _Optional[float] = ...) -> None: ...

class Settings(_message.Message):
    __slots__ = ["sources_list", "services_list", "traffic_type"]
    SOURCES_LIST_FIELD_NUMBER: _ClassVar[int]
    SERVICES_LIST_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    sources_list: _containers.RepeatedScalarFieldContainer[DataSource]
    services_list: _containers.RepeatedScalarFieldContainer[Service]
    traffic_type: TrafficType
    def __init__(self, sources_list: _Optional[_Iterable[_Union[DataSource, str]]] = ..., services_list: _Optional[_Iterable[_Union[Service, str]]] = ..., traffic_type: _Optional[_Union[TrafficType, str]] = ...) -> None: ...

class FiltersList(_message.Message):
    __slots__ = ["airlines_list"]
    class Airline(_message.Message):
        __slots__ = ["icao", "type"]
        ICAO_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        icao: str
        type: int
        def __init__(self, icao: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...
    AIRLINES_LIST_FIELD_NUMBER: _ClassVar[int]
    airlines_list: _containers.RepeatedCompositeFieldContainer[FiltersList.Airline]
    def __init__(self, airlines_list: _Optional[_Iterable[_Union[FiltersList.Airline, _Mapping]]] = ...) -> None: ...

class LiveFeedRequest(_message.Message):
    __slots__ = ["bounds", "settings", "filters_list", "stats", "limit", "maxage", "unknown_msg", "selected_flightid"]
    class UnknownMsg(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAXAGE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_MSG_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHTID_FIELD_NUMBER: _ClassVar[int]
    bounds: Bounds
    settings: Settings
    filters_list: FiltersList
    stats: bool
    limit: int
    maxage: int
    unknown_msg: LiveFeedRequest.UnknownMsg
    selected_flightid: int
    def __init__(self, bounds: _Optional[_Union[Bounds, _Mapping]] = ..., settings: _Optional[_Union[Settings, _Mapping]] = ..., filters_list: _Optional[_Union[FiltersList, _Mapping]] = ..., stats: bool = ..., limit: _Optional[int] = ..., maxage: _Optional[int] = ..., unknown_msg: _Optional[_Union[LiveFeedRequest.UnknownMsg, _Mapping]] = ..., selected_flightid: _Optional[int] = ...) -> None: ...

class LiveFeedResponse(_message.Message):
    __slots__ = ["flights_list", "extra_info"]
    class FlightData(_message.Message):
        __slots__ = ["flightid", "latitude", "longitude", "heading", "altitude", "ground_speed", "icon", "status", "timestamp", "on_ground", "callsign", "source"]
        FLIGHTID_FIELD_NUMBER: _ClassVar[int]
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        ALTITUDE_FIELD_NUMBER: _ClassVar[int]
        GROUND_SPEED_FIELD_NUMBER: _ClassVar[int]
        ICON_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        ON_GROUND_FIELD_NUMBER: _ClassVar[int]
        CALLSIGN_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        flightid: int
        latitude: float
        longitude: float
        heading: int
        altitude: int
        ground_speed: int
        icon: int
        status: int
        timestamp: int
        on_ground: bool
        callsign: str
        source: DataSource
        def __init__(self, flightid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., heading: _Optional[int] = ..., altitude: _Optional[int] = ..., ground_speed: _Optional[int] = ..., icon: _Optional[int] = ..., status: _Optional[int] = ..., timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ...) -> None: ...
    class ExtraInfo(_message.Message):
        __slots__ = ["stats_list"]
        class Stats(_message.Message):
            __slots__ = ["source", "count"]
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            source: DataSource
            count: int
            def __init__(self, source: _Optional[_Union[DataSource, str]] = ..., count: _Optional[int] = ...) -> None: ...
        STATS_LIST_FIELD_NUMBER: _ClassVar[int]
        stats_list: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.ExtraInfo.Stats]
        def __init__(self, stats_list: _Optional[_Iterable[_Union[LiveFeedResponse.ExtraInfo.Stats, _Mapping]]] = ...) -> None: ...
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFO_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.FlightData]
    extra_info: LiveFeedResponse.ExtraInfo
    def __init__(self, flights_list: _Optional[_Iterable[_Union[LiveFeedResponse.FlightData, _Mapping]]] = ..., extra_info: _Optional[_Union[LiveFeedResponse.ExtraInfo, _Mapping]] = ...) -> None: ...
