from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

ADSB: DataSource
AUS: DataSource
BUSINESS_JETS: Service
CARGO: Service
DESCRIPTOR: _descriptor.FileDescriptor
DRONES: Service
ESTIMATED: DataSource
FAA: DataSource
FLARM: DataSource
GENERAL_AVIATION: Service
GLIDERS: Service
GROUND_VEHICLES: Service
HELICOPTERS: Service
LIGHTER_THAN_AIR: Service
MILITARY_AND_GOVERNMENT: Service
MLAT: DataSource
NON_CATEGORIZED: Service
OTHER_DATA_SOURCE: DataSource
OTHER_SERVICE: Service
PASSENGER: Service
SATELLITE: DataSource
SPIDERTRACKS: DataSource
UAT: DataSource

class FiltersList(_message.Message):
    __slots__ = ["airline_filters_list", "airports_list", "altitude_ranges_list", "birth_year_ranges_list", "callsigns_list", "categories_list", "destinations_list", "origins_list", "radars_list", "regs_list", "speed_ranges_list", "types_list"]
    class AirlineFilter(_message.Message):
        __slots__ = ["icao", "type"]
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        ICAO_FIELD_NUMBER: _ClassVar[int]
        OPERATED_AS: FiltersList.AirlineFilter.Type
        PAINTED_AS: FiltersList.AirlineFilter.Type
        TYPE_FIELD_NUMBER: _ClassVar[int]
        icao: str
        type: FiltersList.AirlineFilter.Type
        def __init__(self, icao: _Optional[str] = ..., type: _Optional[_Union[FiltersList.AirlineFilter.Type, str]] = ...) -> None: ...
    class AirportFilter(_message.Message):
        __slots__ = ["country_id", "iata", "type"]
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        BOTH: FiltersList.AirportFilter.Type
        COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        IATA_FIELD_NUMBER: _ClassVar[int]
        INBOUND: FiltersList.AirportFilter.Type
        OUTBOUND: FiltersList.AirportFilter.Type
        TYPE_FIELD_NUMBER: _ClassVar[int]
        country_id: int
        iata: str
        type: FiltersList.AirportFilter.Type
        def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ..., type: _Optional[_Union[FiltersList.AirportFilter.Type, str]] = ...) -> None: ...
    class AltitudeRange(_message.Message):
        __slots__ = ["max", "min"]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        max: int
        min: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class BirthYearRange(_message.Message):
        __slots__ = ["max", "min"]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        max: int
        min: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class ODFilter(_message.Message):
        __slots__ = ["country_id", "iata"]
        COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        IATA_FIELD_NUMBER: _ClassVar[int]
        country_id: int
        iata: str
        def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ...) -> None: ...
    class SpeedRange(_message.Message):
        __slots__ = ["max", "min"]
        MAX_FIELD_NUMBER: _ClassVar[int]
        MIN_FIELD_NUMBER: _ClassVar[int]
        max: int
        min: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    AIRLINE_FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRPORTS_LIST_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    BIRTH_YEAR_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    CALLSIGNS_LIST_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_LIST_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_LIST_FIELD_NUMBER: _ClassVar[int]
    RADARS_LIST_FIELD_NUMBER: _ClassVar[int]
    REGS_LIST_FIELD_NUMBER: _ClassVar[int]
    SPEED_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    TYPES_LIST_FIELD_NUMBER: _ClassVar[int]
    airline_filters_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AirlineFilter]
    airports_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AirportFilter]
    altitude_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AltitudeRange]
    birth_year_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.BirthYearRange]
    callsigns_list: _containers.RepeatedScalarFieldContainer[str]
    categories_list: _containers.RepeatedScalarFieldContainer[Service]
    destinations_list: _containers.RepeatedCompositeFieldContainer[FiltersList.ODFilter]
    origins_list: _containers.RepeatedCompositeFieldContainer[FiltersList.ODFilter]
    radars_list: _containers.RepeatedScalarFieldContainer[str]
    regs_list: _containers.RepeatedScalarFieldContainer[str]
    speed_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.SpeedRange]
    types_list: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, altitude_ranges_list: _Optional[_Iterable[_Union[FiltersList.AltitudeRange, _Mapping]]] = ..., speed_ranges_list: _Optional[_Iterable[_Union[FiltersList.SpeedRange, _Mapping]]] = ..., airline_filters_list: _Optional[_Iterable[_Union[FiltersList.AirlineFilter, _Mapping]]] = ..., callsigns_list: _Optional[_Iterable[str]] = ..., radars_list: _Optional[_Iterable[str]] = ..., regs_list: _Optional[_Iterable[str]] = ..., airports_list: _Optional[_Iterable[_Union[FiltersList.AirportFilter, _Mapping]]] = ..., types_list: _Optional[_Iterable[str]] = ..., birth_year_ranges_list: _Optional[_Iterable[_Union[FiltersList.BirthYearRange, _Mapping]]] = ..., origins_list: _Optional[_Iterable[_Union[FiltersList.ODFilter, _Mapping]]] = ..., destinations_list: _Optional[_Iterable[_Union[FiltersList.ODFilter, _Mapping]]] = ..., categories_list: _Optional[_Iterable[_Union[Service, str]]] = ...) -> None: ...

class LiveFeedPlaybackRequest(_message.Message):
    __slots__ = ["hfreq", "live_feed_request", "prefetch", "timestamp"]
    HFREQ_FIELD_NUMBER: _ClassVar[int]
    LIVE_FEED_REQUEST_FIELD_NUMBER: _ClassVar[int]
    PREFETCH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    hfreq: int
    live_feed_request: LiveFeedRequest
    prefetch: int
    timestamp: int
    def __init__(self, live_feed_request: _Optional[_Union[LiveFeedRequest, _Mapping]] = ..., timestamp: _Optional[int] = ..., prefetch: _Optional[int] = ..., hfreq: _Optional[int] = ...) -> None: ...

class LiveFeedPlaybackResponse(_message.Message):
    __slots__ = ["live_feed_response"]
    LIVE_FEED_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    live_feed_response: LiveFeedResponse
    def __init__(self, live_feed_response: _Optional[_Union[LiveFeedResponse, _Mapping]] = ...) -> None: ...

class LiveFeedRequest(_message.Message):
    __slots__ = ["bounds", "custom_fleet_id", "field_mask", "filters_list", "highlight_mode", "limit", "maxage", "restriction_mode", "selected_flightid", "settings", "stats"]
    class RestrictionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Bounds(_message.Message):
        __slots__ = ["east", "north", "south", "west"]
        EAST_FIELD_NUMBER: _ClassVar[int]
        NORTH_FIELD_NUMBER: _ClassVar[int]
        SOUTH_FIELD_NUMBER: _ClassVar[int]
        WEST_FIELD_NUMBER: _ClassVar[int]
        east: float
        north: float
        south: float
        west: float
        def __init__(self, north: _Optional[float] = ..., south: _Optional[float] = ..., west: _Optional[float] = ..., east: _Optional[float] = ...) -> None: ...
    class FieldMask(_message.Message):
        __slots__ = ["field_name"]
        FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
        field_name: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, field_name: _Optional[_Iterable[str]] = ...) -> None: ...
    class Settings(_message.Message):
        __slots__ = ["only_restricted", "services_list", "sources_list", "traffic_type"]
        class TrafficType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
        AIRBORNE_ONLY: LiveFeedRequest.Settings.TrafficType
        ALL: LiveFeedRequest.Settings.TrafficType
        GROUND_ONLY: LiveFeedRequest.Settings.TrafficType
        NONE: LiveFeedRequest.Settings.TrafficType
        ONLY_RESTRICTED_FIELD_NUMBER: _ClassVar[int]
        SERVICES_LIST_FIELD_NUMBER: _ClassVar[int]
        SOURCES_LIST_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_TYPE_FIELD_NUMBER: _ClassVar[int]
        only_restricted: bool
        services_list: _containers.RepeatedScalarFieldContainer[Service]
        sources_list: _containers.RepeatedScalarFieldContainer[DataSource]
        traffic_type: LiveFeedRequest.Settings.TrafficType
        def __init__(self, sources_list: _Optional[_Iterable[_Union[DataSource, str]]] = ..., services_list: _Optional[_Iterable[_Union[Service, str]]] = ..., traffic_type: _Optional[_Union[LiveFeedRequest.Settings.TrafficType, str]] = ..., only_restricted: bool = ...) -> None: ...
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FLEET_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    HIGHLIGHT_MODE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAXAGE_FIELD_NUMBER: _ClassVar[int]
    NOT_VISIBLE: LiveFeedRequest.RestrictionMode
    RESTRICTED_INCLUDED: LiveFeedRequest.RestrictionMode
    RESTRICTED_ONLY: LiveFeedRequest.RestrictionMode
    RESTRICTION_MODE_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHTID_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    bounds: LiveFeedRequest.Bounds
    custom_fleet_id: str
    field_mask: LiveFeedRequest.FieldMask
    filters_list: FiltersList
    highlight_mode: bool
    limit: int
    maxage: int
    restriction_mode: LiveFeedRequest.RestrictionMode
    selected_flightid: _containers.RepeatedScalarFieldContainer[int]
    settings: LiveFeedRequest.Settings
    stats: bool
    def __init__(self, bounds: _Optional[_Union[LiveFeedRequest.Bounds, _Mapping]] = ..., settings: _Optional[_Union[LiveFeedRequest.Settings, _Mapping]] = ..., filters_list: _Optional[_Union[FiltersList, _Mapping]] = ..., custom_fleet_id: _Optional[str] = ..., highlight_mode: bool = ..., stats: bool = ..., limit: _Optional[int] = ..., maxage: _Optional[int] = ..., restriction_mode: _Optional[_Union[LiveFeedRequest.RestrictionMode, str]] = ..., field_mask: _Optional[_Union[LiveFeedRequest.FieldMask, _Mapping]] = ..., selected_flightid: _Optional[_Iterable[int]] = ...) -> None: ...

class LiveFeedResponse(_message.Message):
    __slots__ = ["flights_list", "selected_flight_info", "stats"]
    class FlightData(_message.Message):
        __slots__ = ["altitude", "callsign", "extra_info", "flightid", "ground_speed", "heading", "icon", "latitude", "longitude", "on_ground", "source", "status", "timestamp"]
        class ExtraInfo(_message.Message):
            __slots__ = ["ac_birthday", "airspace", "country_of_reg", "ems_availability", "ems_info", "flight", "icao_address", "logo_id", "reg", "route", "schedule", "squawk", "type", "vspeed"]
            class EMS(_message.Message):
                __slots__ = ["afms", "agps", "agpsdiff", "amcp", "apflags", "ias", "mach", "oat", "qnh", "rs", "tas", "wind_dir", "wind_speed"]
                AFMS_FIELD_NUMBER: _ClassVar[int]
                AGPSDIFF_FIELD_NUMBER: _ClassVar[int]
                AGPS_FIELD_NUMBER: _ClassVar[int]
                AMCP_FIELD_NUMBER: _ClassVar[int]
                APFLAGS_FIELD_NUMBER: _ClassVar[int]
                IAS_FIELD_NUMBER: _ClassVar[int]
                MACH_FIELD_NUMBER: _ClassVar[int]
                OAT_FIELD_NUMBER: _ClassVar[int]
                QNH_FIELD_NUMBER: _ClassVar[int]
                RS_FIELD_NUMBER: _ClassVar[int]
                TAS_FIELD_NUMBER: _ClassVar[int]
                WIND_DIR_FIELD_NUMBER: _ClassVar[int]
                WIND_SPEED_FIELD_NUMBER: _ClassVar[int]
                afms: int
                agps: int
                agpsdiff: int
                amcp: int
                apflags: int
                ias: int
                mach: int
                oat: int
                qnh: int
                rs: int
                tas: int
                wind_dir: int
                wind_speed: int
                def __init__(self, qnh: _Optional[int] = ..., amcp: _Optional[int] = ..., afms: _Optional[int] = ..., oat: _Optional[int] = ..., ias: _Optional[int] = ..., tas: _Optional[int] = ..., mach: _Optional[int] = ..., agps: _Optional[int] = ..., agpsdiff: _Optional[int] = ..., apflags: _Optional[int] = ..., wind_dir: _Optional[int] = ..., wind_speed: _Optional[int] = ..., rs: _Optional[int] = ...) -> None: ...
            class EMSAvailability(_message.Message):
                __slots__ = ["afms_availability", "agps_availability", "agpsdiff_availability", "amcp_availability", "apflags_availability", "ias_availability", "mach_availability", "oat_availability", "qnh_availability", "rs_availability", "tas_availability", "wind_dir_availability", "wind_speed_availability"]
                AFMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AGPSDIFF_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AGPS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AMCP_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                APFLAGS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                IAS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                MACH_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                OAT_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                QNH_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                RS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                TAS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                WIND_DIR_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                WIND_SPEED_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                afms_availability: bool
                agps_availability: bool
                agpsdiff_availability: bool
                amcp_availability: bool
                apflags_availability: bool
                ias_availability: bool
                mach_availability: bool
                oat_availability: bool
                qnh_availability: bool
                rs_availability: bool
                tas_availability: bool
                wind_dir_availability: bool
                wind_speed_availability: bool
                def __init__(self, qnh_availability: bool = ..., amcp_availability: bool = ..., afms_availability: bool = ..., oat_availability: bool = ..., ias_availability: bool = ..., tas_availability: bool = ..., mach_availability: bool = ..., agps_availability: bool = ..., agpsdiff_availability: bool = ..., apflags_availability: bool = ..., wind_dir_availability: bool = ..., wind_speed_availability: bool = ..., rs_availability: bool = ...) -> None: ...
            class Route(_message.Message):
                __slots__ = ["from_", "to"]
                FROM__FIELD_NUMBER: _ClassVar[int]
                TO_FIELD_NUMBER: _ClassVar[int]
                from_: str
                to: str
                def __init__(self, from_: _Optional[str] = ..., to: _Optional[str] = ...) -> None: ...
            class Schedule(_message.Message):
                __slots__ = ["ata", "atd", "eta", "etd", "sta", "std"]
                ATA_FIELD_NUMBER: _ClassVar[int]
                ATD_FIELD_NUMBER: _ClassVar[int]
                ETA_FIELD_NUMBER: _ClassVar[int]
                ETD_FIELD_NUMBER: _ClassVar[int]
                STA_FIELD_NUMBER: _ClassVar[int]
                STD_FIELD_NUMBER: _ClassVar[int]
                ata: int
                atd: int
                eta: int
                etd: int
                sta: int
                std: int
                def __init__(self, std: _Optional[int] = ..., etd: _Optional[int] = ..., atd: _Optional[int] = ..., sta: _Optional[int] = ..., eta: _Optional[int] = ..., ata: _Optional[int] = ...) -> None: ...
            AC_BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
            AIRSPACE_FIELD_NUMBER: _ClassVar[int]
            COUNTRY_OF_REG_FIELD_NUMBER: _ClassVar[int]
            EMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
            EMS_INFO_FIELD_NUMBER: _ClassVar[int]
            FLIGHT_FIELD_NUMBER: _ClassVar[int]
            ICAO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
            LOGO_ID_FIELD_NUMBER: _ClassVar[int]
            REG_FIELD_NUMBER: _ClassVar[int]
            ROUTE_FIELD_NUMBER: _ClassVar[int]
            SCHEDULE_FIELD_NUMBER: _ClassVar[int]
            SQUAWK_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            VSPEED_FIELD_NUMBER: _ClassVar[int]
            ac_birthday: str
            airspace: int
            country_of_reg: int
            ems_availability: LiveFeedResponse.FlightData.ExtraInfo.EMSAvailability
            ems_info: LiveFeedResponse.FlightData.ExtraInfo.EMS
            flight: str
            icao_address: int
            logo_id: int
            reg: str
            route: LiveFeedResponse.FlightData.ExtraInfo.Route
            schedule: LiveFeedResponse.FlightData.ExtraInfo.Schedule
            squawk: int
            type: str
            vspeed: int
            def __init__(self, flight: _Optional[str] = ..., reg: _Optional[str] = ..., route: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.Route, _Mapping]] = ..., type: _Optional[str] = ..., squawk: _Optional[int] = ..., vspeed: _Optional[int] = ..., ac_birthday: _Optional[str] = ..., country_of_reg: _Optional[int] = ..., schedule: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.Schedule, _Mapping]] = ..., logo_id: _Optional[int] = ..., airspace: _Optional[int] = ..., ems_info: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.EMS, _Mapping]] = ..., ems_availability: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.EMSAvailability, _Mapping]] = ..., icao_address: _Optional[int] = ...) -> None: ...
        ALTITUDE_FIELD_NUMBER: _ClassVar[int]
        CALLSIGN_FIELD_NUMBER: _ClassVar[int]
        EXTRA_INFO_FIELD_NUMBER: _ClassVar[int]
        FLIGHTID_FIELD_NUMBER: _ClassVar[int]
        GROUND_SPEED_FIELD_NUMBER: _ClassVar[int]
        HEADING_FIELD_NUMBER: _ClassVar[int]
        ICON_FIELD_NUMBER: _ClassVar[int]
        LATITUDE_FIELD_NUMBER: _ClassVar[int]
        LONGITUDE_FIELD_NUMBER: _ClassVar[int]
        ON_GROUND_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        STATUS_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
        altitude: int
        callsign: str
        extra_info: LiveFeedResponse.FlightData.ExtraInfo
        flightid: int
        ground_speed: int
        heading: int
        icon: int
        latitude: float
        longitude: float
        on_ground: bool
        source: DataSource
        status: int
        timestamp: int
        def __init__(self, flightid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., heading: _Optional[int] = ..., altitude: _Optional[int] = ..., ground_speed: _Optional[int] = ..., icon: _Optional[int] = ..., status: _Optional[int] = ..., timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ..., extra_info: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo, _Mapping]] = ...) -> None: ...
    class Statistics(_message.Message):
        __slots__ = ["sources"]
        class SourceKV(_message.Message):
            __slots__ = ["count", "source"]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            count: int
            source: DataSource
            def __init__(self, source: _Optional[_Union[DataSource, str]] = ..., count: _Optional[int] = ...) -> None: ...
        SOURCES_FIELD_NUMBER: _ClassVar[int]
        sources: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.Statistics.SourceKV]
        def __init__(self, sources: _Optional[_Iterable[_Union[LiveFeedResponse.Statistics.SourceKV, _Mapping]]] = ...) -> None: ...
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHT_INFO_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.FlightData]
    selected_flight_info: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.FlightData]
    stats: LiveFeedResponse.Statistics
    def __init__(self, flights_list: _Optional[_Iterable[_Union[LiveFeedResponse.FlightData, _Mapping]]] = ..., stats: _Optional[_Union[LiveFeedResponse.Statistics, _Mapping]] = ..., selected_flight_info: _Optional[_Iterable[_Union[LiveFeedResponse.FlightData, _Mapping]]] = ...) -> None: ...

class Service(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DataSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
