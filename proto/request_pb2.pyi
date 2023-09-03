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

class FiltersList(_message.Message):
    __slots__ = ["altitude_ranges_list", "speed_ranges_list", "airline_filters_list", "callsigns_list", "radars_list", "regs_list", "airports_list", "types_list", "birth_year_ranges_list", "origins_list", "destinations_list", "categories_list"]
    class AltitudeRange(_message.Message):
        __slots__ = ["min", "max"]
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class SpeedRange(_message.Message):
        __slots__ = ["min", "max"]
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class AirlineFilter(_message.Message):
        __slots__ = ["icao", "type"]
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            PAINTED_AS: _ClassVar[FiltersList.AirlineFilter.Type]
            OPERATED_AS: _ClassVar[FiltersList.AirlineFilter.Type]
        PAINTED_AS: FiltersList.AirlineFilter.Type
        OPERATED_AS: FiltersList.AirlineFilter.Type
        ICAO_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        icao: str
        type: FiltersList.AirlineFilter.Type
        def __init__(self, icao: _Optional[str] = ..., type: _Optional[_Union[FiltersList.AirlineFilter.Type, str]] = ...) -> None: ...
    class AirportFilter(_message.Message):
        __slots__ = ["iata", "country_id", "type"]
        class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            BOTH: _ClassVar[FiltersList.AirportFilter.Type]
            INBOUND: _ClassVar[FiltersList.AirportFilter.Type]
            OUTBOUND: _ClassVar[FiltersList.AirportFilter.Type]
        BOTH: FiltersList.AirportFilter.Type
        INBOUND: FiltersList.AirportFilter.Type
        OUTBOUND: FiltersList.AirportFilter.Type
        IATA_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        iata: str
        country_id: int
        type: FiltersList.AirportFilter.Type
        def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ..., type: _Optional[_Union[FiltersList.AirportFilter.Type, str]] = ...) -> None: ...
    class BirthYearRange(_message.Message):
        __slots__ = ["min", "max"]
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class ODFilter(_message.Message):
        __slots__ = ["iata", "country_id"]
        IATA_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        iata: str
        country_id: int
        def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ...) -> None: ...
    ALTITUDE_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    SPEED_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRLINE_FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    CALLSIGNS_LIST_FIELD_NUMBER: _ClassVar[int]
    RADARS_LIST_FIELD_NUMBER: _ClassVar[int]
    REGS_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRPORTS_LIST_FIELD_NUMBER: _ClassVar[int]
    TYPES_LIST_FIELD_NUMBER: _ClassVar[int]
    BIRTH_YEAR_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_LIST_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_LIST_FIELD_NUMBER: _ClassVar[int]
    altitude_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AltitudeRange]
    speed_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.SpeedRange]
    airline_filters_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AirlineFilter]
    callsigns_list: _containers.RepeatedScalarFieldContainer[str]
    radars_list: _containers.RepeatedScalarFieldContainer[str]
    regs_list: _containers.RepeatedScalarFieldContainer[str]
    airports_list: _containers.RepeatedCompositeFieldContainer[FiltersList.AirportFilter]
    types_list: _containers.RepeatedScalarFieldContainer[str]
    birth_year_ranges_list: _containers.RepeatedCompositeFieldContainer[FiltersList.BirthYearRange]
    origins_list: _containers.RepeatedCompositeFieldContainer[FiltersList.ODFilter]
    destinations_list: _containers.RepeatedCompositeFieldContainer[FiltersList.ODFilter]
    categories_list: _containers.RepeatedScalarFieldContainer[Service]
    def __init__(self, altitude_ranges_list: _Optional[_Iterable[_Union[FiltersList.AltitudeRange, _Mapping]]] = ..., speed_ranges_list: _Optional[_Iterable[_Union[FiltersList.SpeedRange, _Mapping]]] = ..., airline_filters_list: _Optional[_Iterable[_Union[FiltersList.AirlineFilter, _Mapping]]] = ..., callsigns_list: _Optional[_Iterable[str]] = ..., radars_list: _Optional[_Iterable[str]] = ..., regs_list: _Optional[_Iterable[str]] = ..., airports_list: _Optional[_Iterable[_Union[FiltersList.AirportFilter, _Mapping]]] = ..., types_list: _Optional[_Iterable[str]] = ..., birth_year_ranges_list: _Optional[_Iterable[_Union[FiltersList.BirthYearRange, _Mapping]]] = ..., origins_list: _Optional[_Iterable[_Union[FiltersList.ODFilter, _Mapping]]] = ..., destinations_list: _Optional[_Iterable[_Union[FiltersList.ODFilter, _Mapping]]] = ..., categories_list: _Optional[_Iterable[_Union[Service, str]]] = ...) -> None: ...

class LiveFeedRequest(_message.Message):
    __slots__ = ["bounds", "settings", "filters_list", "custom_fleet_id", "stats", "limit", "maxage", "field_mask", "selected_flightid"]
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
        class TrafficType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            NONE: _ClassVar[LiveFeedRequest.Settings.TrafficType]
            GROUND_ONLY: _ClassVar[LiveFeedRequest.Settings.TrafficType]
            AIRBORNE_ONLY: _ClassVar[LiveFeedRequest.Settings.TrafficType]
            ALL: _ClassVar[LiveFeedRequest.Settings.TrafficType]
        NONE: LiveFeedRequest.Settings.TrafficType
        GROUND_ONLY: LiveFeedRequest.Settings.TrafficType
        AIRBORNE_ONLY: LiveFeedRequest.Settings.TrafficType
        ALL: LiveFeedRequest.Settings.TrafficType
        SOURCES_LIST_FIELD_NUMBER: _ClassVar[int]
        SERVICES_LIST_FIELD_NUMBER: _ClassVar[int]
        TRAFFIC_TYPE_FIELD_NUMBER: _ClassVar[int]
        sources_list: _containers.RepeatedScalarFieldContainer[DataSource]
        services_list: _containers.RepeatedScalarFieldContainer[Service]
        traffic_type: LiveFeedRequest.Settings.TrafficType
        def __init__(self, sources_list: _Optional[_Iterable[_Union[DataSource, str]]] = ..., services_list: _Optional[_Iterable[_Union[Service, str]]] = ..., traffic_type: _Optional[_Union[LiveFeedRequest.Settings.TrafficType, str]] = ...) -> None: ...
    class FieldMask(_message.Message):
        __slots__ = ["field_name"]
        FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
        field_name: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, field_name: _Optional[_Iterable[str]] = ...) -> None: ...
    BOUNDS_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    FILTERS_LIST_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_FLEET_ID_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    MAXAGE_FIELD_NUMBER: _ClassVar[int]
    FIELD_MASK_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHTID_FIELD_NUMBER: _ClassVar[int]
    bounds: LiveFeedRequest.Bounds
    settings: LiveFeedRequest.Settings
    filters_list: FiltersList
    custom_fleet_id: str
    stats: bool
    limit: int
    maxage: int
    field_mask: LiveFeedRequest.FieldMask
    selected_flightid: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, bounds: _Optional[_Union[LiveFeedRequest.Bounds, _Mapping]] = ..., settings: _Optional[_Union[LiveFeedRequest.Settings, _Mapping]] = ..., filters_list: _Optional[_Union[FiltersList, _Mapping]] = ..., custom_fleet_id: _Optional[str] = ..., stats: bool = ..., limit: _Optional[int] = ..., maxage: _Optional[int] = ..., field_mask: _Optional[_Union[LiveFeedRequest.FieldMask, _Mapping]] = ..., selected_flightid: _Optional[_Iterable[int]] = ...) -> None: ...

class LiveFeedResponse(_message.Message):
    __slots__ = ["flights_list", "stats", "selected_flight_info"]
    class FlightData(_message.Message):
        __slots__ = ["flightid", "latitude", "longitude", "heading", "altitude", "ground_speed", "icon", "status", "timestamp", "on_ground", "callsign", "source", "extra_info"]
        class ExtraInfo(_message.Message):
            __slots__ = ["flight", "reg", "route", "type", "squawk", "vspeed", "ac_birthday", "country_of_reg", "schedule", "logo_id", "airspace", "ems_info", "ems_availability"]
            class Route(_message.Message):
                __slots__ = ["to"]
                FROM_FIELD_NUMBER: _ClassVar[int]
                TO_FIELD_NUMBER: _ClassVar[int]
                to: str
                def __init__(self, to: _Optional[str] = ..., **kwargs) -> None: ...
            class Schedule(_message.Message):
                __slots__ = ["std", "etd", "atd", "sta", "eta", "ata"]
                STD_FIELD_NUMBER: _ClassVar[int]
                ETD_FIELD_NUMBER: _ClassVar[int]
                ATD_FIELD_NUMBER: _ClassVar[int]
                STA_FIELD_NUMBER: _ClassVar[int]
                ETA_FIELD_NUMBER: _ClassVar[int]
                ATA_FIELD_NUMBER: _ClassVar[int]
                std: int
                etd: int
                atd: int
                sta: int
                eta: int
                ata: int
                def __init__(self, std: _Optional[int] = ..., etd: _Optional[int] = ..., atd: _Optional[int] = ..., sta: _Optional[int] = ..., eta: _Optional[int] = ..., ata: _Optional[int] = ...) -> None: ...
            class EMS(_message.Message):
                __slots__ = ["qnh", "amcp", "afms", "oat", "ias", "tas", "mach", "agps", "agpsdiff", "apflags", "wind_dir", "wind_speed", "rs"]
                QNH_FIELD_NUMBER: _ClassVar[int]
                AMCP_FIELD_NUMBER: _ClassVar[int]
                AFMS_FIELD_NUMBER: _ClassVar[int]
                OAT_FIELD_NUMBER: _ClassVar[int]
                IAS_FIELD_NUMBER: _ClassVar[int]
                TAS_FIELD_NUMBER: _ClassVar[int]
                MACH_FIELD_NUMBER: _ClassVar[int]
                AGPS_FIELD_NUMBER: _ClassVar[int]
                AGPSDIFF_FIELD_NUMBER: _ClassVar[int]
                APFLAGS_FIELD_NUMBER: _ClassVar[int]
                WIND_DIR_FIELD_NUMBER: _ClassVar[int]
                WIND_SPEED_FIELD_NUMBER: _ClassVar[int]
                RS_FIELD_NUMBER: _ClassVar[int]
                qnh: int
                amcp: int
                afms: int
                oat: int
                ias: int
                tas: int
                mach: int
                agps: int
                agpsdiff: int
                apflags: int
                wind_dir: int
                wind_speed: int
                rs: int
                def __init__(self, qnh: _Optional[int] = ..., amcp: _Optional[int] = ..., afms: _Optional[int] = ..., oat: _Optional[int] = ..., ias: _Optional[int] = ..., tas: _Optional[int] = ..., mach: _Optional[int] = ..., agps: _Optional[int] = ..., agpsdiff: _Optional[int] = ..., apflags: _Optional[int] = ..., wind_dir: _Optional[int] = ..., wind_speed: _Optional[int] = ..., rs: _Optional[int] = ...) -> None: ...
            class EMSAvailability(_message.Message):
                __slots__ = ["qnh_availability", "amcp_availability", "afms_availability", "oat_availability", "ias_availability", "tas_availability", "mach_availability", "agps_availability", "agpsdiff_availability", "apflags_availability", "wind_dir_availability", "wind_speed_availability", "rs_availability"]
                QNH_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AMCP_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AFMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                OAT_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                IAS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                TAS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                MACH_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AGPS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                AGPSDIFF_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                APFLAGS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                WIND_DIR_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                WIND_SPEED_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                RS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
                qnh_availability: bool
                amcp_availability: bool
                afms_availability: bool
                oat_availability: bool
                ias_availability: bool
                tas_availability: bool
                mach_availability: bool
                agps_availability: bool
                agpsdiff_availability: bool
                apflags_availability: bool
                wind_dir_availability: bool
                wind_speed_availability: bool
                rs_availability: bool
                def __init__(self, qnh_availability: bool = ..., amcp_availability: bool = ..., afms_availability: bool = ..., oat_availability: bool = ..., ias_availability: bool = ..., tas_availability: bool = ..., mach_availability: bool = ..., agps_availability: bool = ..., agpsdiff_availability: bool = ..., apflags_availability: bool = ..., wind_dir_availability: bool = ..., wind_speed_availability: bool = ..., rs_availability: bool = ...) -> None: ...
            FLIGHT_FIELD_NUMBER: _ClassVar[int]
            REG_FIELD_NUMBER: _ClassVar[int]
            ROUTE_FIELD_NUMBER: _ClassVar[int]
            TYPE_FIELD_NUMBER: _ClassVar[int]
            SQUAWK_FIELD_NUMBER: _ClassVar[int]
            VSPEED_FIELD_NUMBER: _ClassVar[int]
            AC_BIRTHDAY_FIELD_NUMBER: _ClassVar[int]
            COUNTRY_OF_REG_FIELD_NUMBER: _ClassVar[int]
            SCHEDULE_FIELD_NUMBER: _ClassVar[int]
            LOGO_ID_FIELD_NUMBER: _ClassVar[int]
            AIRSPACE_FIELD_NUMBER: _ClassVar[int]
            EMS_INFO_FIELD_NUMBER: _ClassVar[int]
            EMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
            flight: str
            reg: str
            route: LiveFeedResponse.FlightData.ExtraInfo.Route
            type: str
            squawk: int
            vspeed: int
            ac_birthday: str
            country_of_reg: int
            schedule: LiveFeedResponse.FlightData.ExtraInfo.Schedule
            logo_id: int
            airspace: int
            ems_info: LiveFeedResponse.FlightData.ExtraInfo.EMS
            ems_availability: LiveFeedResponse.FlightData.ExtraInfo.EMSAvailability
            def __init__(self, flight: _Optional[str] = ..., reg: _Optional[str] = ..., route: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.Route, _Mapping]] = ..., type: _Optional[str] = ..., squawk: _Optional[int] = ..., vspeed: _Optional[int] = ..., ac_birthday: _Optional[str] = ..., country_of_reg: _Optional[int] = ..., schedule: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.Schedule, _Mapping]] = ..., logo_id: _Optional[int] = ..., airspace: _Optional[int] = ..., ems_info: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.EMS, _Mapping]] = ..., ems_availability: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo.EMSAvailability, _Mapping]] = ...) -> None: ...
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
        EXTRA_INFO_FIELD_NUMBER: _ClassVar[int]
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
        extra_info: LiveFeedResponse.FlightData.ExtraInfo
        def __init__(self, flightid: _Optional[int] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., heading: _Optional[int] = ..., altitude: _Optional[int] = ..., ground_speed: _Optional[int] = ..., icon: _Optional[int] = ..., status: _Optional[int] = ..., timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ..., extra_info: _Optional[_Union[LiveFeedResponse.FlightData.ExtraInfo, _Mapping]] = ...) -> None: ...
    class Statistics(_message.Message):
        __slots__ = ["sources"]
        class SourceKV(_message.Message):
            __slots__ = ["source", "count"]
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            COUNT_FIELD_NUMBER: _ClassVar[int]
            source: DataSource
            count: int
            def __init__(self, source: _Optional[_Union[DataSource, str]] = ..., count: _Optional[int] = ...) -> None: ...
        SOURCES_FIELD_NUMBER: _ClassVar[int]
        sources: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.Statistics.SourceKV]
        def __init__(self, sources: _Optional[_Iterable[_Union[LiveFeedResponse.Statistics.SourceKV, _Mapping]]] = ...) -> None: ...
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHT_INFO_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.FlightData]
    stats: LiveFeedResponse.Statistics
    selected_flight_info: _containers.RepeatedCompositeFieldContainer[LiveFeedResponse.FlightData]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[LiveFeedResponse.FlightData, _Mapping]]] = ..., stats: _Optional[_Union[LiveFeedResponse.Statistics, _Mapping]] = ..., selected_flight_info: _Optional[_Iterable[_Union[LiveFeedResponse.FlightData, _Mapping]]] = ...) -> None: ...
