from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RestrictionVisibility(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NOT_VISIBLE: _ClassVar[RestrictionVisibility]
    PARTIALLY_VISIBLE: _ClassVar[RestrictionVisibility]
    FULLY_VISIBLE: _ClassVar[RestrictionVisibility]

class Service(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
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

class AirportFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    BOTH: _ClassVar[AirportFilterType]
    INBOUND: _ClassVar[AirportFilterType]
    OUTBOUND: _ClassVar[AirportFilterType]

class AirlineFilterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAINTED_AS: _ClassVar[AirlineFilterType]
    OPERATED_AS: _ClassVar[AirlineFilterType]

class TrafficType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NONE: _ClassVar[TrafficType]
    GROUND_ONLY: _ClassVar[TrafficType]
    AIRBORNE_ONLY: _ClassVar[TrafficType]
    ALL: _ClassVar[TrafficType]

class DataSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
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

class Icon(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    B738: _ClassVar[Icon]
    FGTR: _ClassVar[Icon]
    ASW20: _ClassVar[Icon]
    C206: _ClassVar[Icon]
    C303: _ClassVar[Icon]
    LJ60: _ClassVar[Icon]
    Q300: _ClassVar[Icon]
    B736: _ClassVar[Icon]
    FOKKER100: _ClassVar[Icon]
    RJ85: _ClassVar[Icon]
    A320: _ClassVar[Icon]
    B757: _ClassVar[Icon]
    B767: _ClassVar[Icon]
    A3ST: _ClassVar[Icon]
    MD11: _ClassVar[Icon]
    A330: _ClassVar[Icon]
    A343: _ClassVar[Icon]
    A346: _ClassVar[Icon]
    B777: _ClassVar[Icon]
    B747: _ClassVar[Icon]
    A380: _ClassVar[Icon]
    A225: _ClassVar[Icon]
    SI2: _ClassVar[Icon]
    EC: _ClassVar[Icon]
    BALL: _ClassVar[Icon]
    GRND: _ClassVar[Icon]
    SLEI: _ClassVar[Icon]
    DRON: _ClassVar[Icon]
    SAT: _ClassVar[Icon]
    ISS: _ClassVar[Icon]

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NORMAL: _ClassVar[Status]
    BACKGROUND: _ClassVar[Status]
    EMERGENCY: _ClassVar[Status]
    NOT_AVAILABLE: _ClassVar[Status]
    LIVE: _ClassVar[Status]

class EmergencyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_EMERGENCY: _ClassVar[EmergencyStatus]
    GENERAL_EMERGENCY: _ClassVar[EmergencyStatus]
    LIFEGUARD_MEDICAL_EMERGENCY: _ClassVar[EmergencyStatus]
    MINIMUM_FUEL: _ClassVar[EmergencyStatus]
    NO_COMMUNICATIONS: _ClassVar[EmergencyStatus]
    UNLAWFUL_INTERFERENCE: _ClassVar[EmergencyStatus]
    DOWNED_AIRCRAFT: _ClassVar[EmergencyStatus]
    RESERVED: _ClassVar[EmergencyStatus]

class FlightStage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[FlightStage]
    ON_GROUND: _ClassVar[FlightStage]
    TAKING_OFF: _ClassVar[FlightStage]
    AIRBORNE: _ClassVar[FlightStage]
    ON_APPROACH: _ClassVar[FlightStage]
NOT_VISIBLE: RestrictionVisibility
PARTIALLY_VISIBLE: RestrictionVisibility
FULLY_VISIBLE: RestrictionVisibility
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
BOTH: AirportFilterType
INBOUND: AirportFilterType
OUTBOUND: AirportFilterType
PAINTED_AS: AirlineFilterType
OPERATED_AS: AirlineFilterType
NONE: TrafficType
GROUND_ONLY: TrafficType
AIRBORNE_ONLY: TrafficType
ALL: TrafficType
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
B738: Icon
FGTR: Icon
ASW20: Icon
C206: Icon
C303: Icon
LJ60: Icon
Q300: Icon
B736: Icon
FOKKER100: Icon
RJ85: Icon
A320: Icon
B757: Icon
B767: Icon
A3ST: Icon
MD11: Icon
A330: Icon
A343: Icon
A346: Icon
B777: Icon
B747: Icon
A380: Icon
A225: Icon
SI2: Icon
EC: Icon
BALL: Icon
GRND: Icon
SLEI: Icon
DRON: Icon
SAT: Icon
ISS: Icon
NORMAL: Status
BACKGROUND: Status
EMERGENCY: Status
NOT_AVAILABLE: Status
LIVE: Status
NO_EMERGENCY: EmergencyStatus
GENERAL_EMERGENCY: EmergencyStatus
LIFEGUARD_MEDICAL_EMERGENCY: EmergencyStatus
MINIMUM_FUEL: EmergencyStatus
NO_COMMUNICATIONS: EmergencyStatus
UNLAWFUL_INTERFERENCE: EmergencyStatus
DOWNED_AIRCRAFT: EmergencyStatus
RESERVED: EmergencyStatus
UNKNOWN: FlightStage
ON_GROUND: FlightStage
TAKING_OFF: FlightStage
AIRBORNE: FlightStage
ON_APPROACH: FlightStage

class AirportFilter(_message.Message):
    __slots__ = ("iata", "country_id", "type")
    IATA_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    iata: str
    country_id: int
    type: AirportFilterType
    def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ..., type: _Optional[_Union[AirportFilterType, str]] = ...) -> None: ...

class AirlineFilter(_message.Message):
    __slots__ = ("icao", "type")
    ICAO_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    icao: str
    type: AirlineFilterType
    def __init__(self, icao: _Optional[str] = ..., type: _Optional[_Union[AirlineFilterType, str]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("altitude_ranges_list", "speed_ranges_list", "airlines_list", "callsigns_list", "radars_list", "regs_list", "airports_list", "types_list", "birth_year_ranges_list", "origins_list", "destinations_list", "categories_list")
    class AltitudeRange(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class SpeedRange(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class BirthYearRange(_message.Message):
        __slots__ = ("min", "max")
        MIN_FIELD_NUMBER: _ClassVar[int]
        MAX_FIELD_NUMBER: _ClassVar[int]
        min: int
        max: int
        def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...
    class ODFilter(_message.Message):
        __slots__ = ("iata", "country_id")
        IATA_FIELD_NUMBER: _ClassVar[int]
        COUNTRY_ID_FIELD_NUMBER: _ClassVar[int]
        iata: str
        country_id: int
        def __init__(self, iata: _Optional[str] = ..., country_id: _Optional[int] = ...) -> None: ...
    ALTITUDE_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    SPEED_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRLINES_LIST_FIELD_NUMBER: _ClassVar[int]
    CALLSIGNS_LIST_FIELD_NUMBER: _ClassVar[int]
    RADARS_LIST_FIELD_NUMBER: _ClassVar[int]
    REGS_LIST_FIELD_NUMBER: _ClassVar[int]
    AIRPORTS_LIST_FIELD_NUMBER: _ClassVar[int]
    TYPES_LIST_FIELD_NUMBER: _ClassVar[int]
    BIRTH_YEAR_RANGES_LIST_FIELD_NUMBER: _ClassVar[int]
    ORIGINS_LIST_FIELD_NUMBER: _ClassVar[int]
    DESTINATIONS_LIST_FIELD_NUMBER: _ClassVar[int]
    CATEGORIES_LIST_FIELD_NUMBER: _ClassVar[int]
    altitude_ranges_list: _containers.RepeatedCompositeFieldContainer[Filter.AltitudeRange]
    speed_ranges_list: _containers.RepeatedCompositeFieldContainer[Filter.SpeedRange]
    airlines_list: _containers.RepeatedCompositeFieldContainer[AirlineFilter]
    callsigns_list: _containers.RepeatedScalarFieldContainer[str]
    radars_list: _containers.RepeatedScalarFieldContainer[str]
    regs_list: _containers.RepeatedScalarFieldContainer[str]
    airports_list: _containers.RepeatedCompositeFieldContainer[AirportFilter]
    types_list: _containers.RepeatedScalarFieldContainer[str]
    birth_year_ranges_list: _containers.RepeatedCompositeFieldContainer[Filter.BirthYearRange]
    origins_list: _containers.RepeatedCompositeFieldContainer[Filter.ODFilter]
    destinations_list: _containers.RepeatedCompositeFieldContainer[Filter.ODFilter]
    categories_list: _containers.RepeatedScalarFieldContainer[Service]
    def __init__(self, altitude_ranges_list: _Optional[_Iterable[_Union[Filter.AltitudeRange, _Mapping]]] = ..., speed_ranges_list: _Optional[_Iterable[_Union[Filter.SpeedRange, _Mapping]]] = ..., airlines_list: _Optional[_Iterable[_Union[AirlineFilter, _Mapping]]] = ..., callsigns_list: _Optional[_Iterable[str]] = ..., radars_list: _Optional[_Iterable[str]] = ..., regs_list: _Optional[_Iterable[str]] = ..., airports_list: _Optional[_Iterable[_Union[AirportFilter, _Mapping]]] = ..., types_list: _Optional[_Iterable[str]] = ..., birth_year_ranges_list: _Optional[_Iterable[_Union[Filter.BirthYearRange, _Mapping]]] = ..., origins_list: _Optional[_Iterable[_Union[Filter.ODFilter, _Mapping]]] = ..., destinations_list: _Optional[_Iterable[_Union[Filter.ODFilter, _Mapping]]] = ..., categories_list: _Optional[_Iterable[_Union[Service, str]]] = ...) -> None: ...

class VisibilitySettings(_message.Message):
    __slots__ = ("sources_list", "services_list", "traffic_type", "only_restricted")
    SOURCES_LIST_FIELD_NUMBER: _ClassVar[int]
    SERVICES_LIST_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    ONLY_RESTRICTED_FIELD_NUMBER: _ClassVar[int]
    sources_list: _containers.RepeatedScalarFieldContainer[DataSource]
    services_list: _containers.RepeatedScalarFieldContainer[Service]
    traffic_type: TrafficType
    only_restricted: bool
    def __init__(self, sources_list: _Optional[_Iterable[_Union[DataSource, str]]] = ..., services_list: _Optional[_Iterable[_Union[Service, str]]] = ..., traffic_type: _Optional[_Union[TrafficType, str]] = ..., only_restricted: bool = ...) -> None: ...

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

class LiveFeedRequest(_message.Message):
    __slots__ = ("bounds", "settings", "filters_list", "fleets_list", "highlight_mode", "stats", "limit", "maxage", "restriction_mode", "field_mask", "selected_flight_ids_list")
    class FieldMask(_message.Message):
        __slots__ = ("field_name",)
        FIELD_NAME_FIELD_NUMBER: _ClassVar[int]
        field_name: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, field_name: _Optional[_Iterable[str]] = ...) -> None: ...
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
    restriction_mode: RestrictionVisibility
    field_mask: LiveFeedRequest.FieldMask
    selected_flight_ids_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, bounds: _Optional[_Union[LocationBoundaries, _Mapping]] = ..., settings: _Optional[_Union[VisibilitySettings, _Mapping]] = ..., filters_list: _Optional[_Union[Filter, _Mapping]] = ..., fleets_list: _Optional[str] = ..., highlight_mode: bool = ..., stats: bool = ..., limit: _Optional[int] = ..., maxage: _Optional[int] = ..., restriction_mode: _Optional[_Union[RestrictionVisibility, str]] = ..., field_mask: _Optional[_Union[LiveFeedRequest.FieldMask, _Mapping]] = ..., selected_flight_ids_list: _Optional[_Iterable[int]] = ...) -> None: ...

class EMSInfo(_message.Message):
    __slots__ = ("qnh", "amcp", "afms", "oat", "ias", "tas", "mach", "agps", "agpsdiff", "apflags", "wind_dir", "wind_speed", "rs")
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
    __slots__ = ("qnh_availability", "amcp_availability", "afms_availability", "oat_availability", "ias_availability", "tas_availability", "mach_availability", "agps_availability", "agpsdiff_availability", "apflags_availability", "wind_dir_availability", "wind_speed_availability", "rs_availability")
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

class Schedule(_message.Message):
    __slots__ = ("std", "etd", "atd", "sta", "eta", "ata")
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

class ExtraFlightInfo(_message.Message):
    __slots__ = ("flight", "reg", "route", "type", "squawk", "vspeed", "age", "country_of_reg", "schedule", "logo_id", "airspace", "ems_info", "ems_availability", "icao_address")
    class Route(_message.Message):
        __slots__ = ("from_", "to")
        FROM__FIELD_NUMBER: _ClassVar[int]
        TO_FIELD_NUMBER: _ClassVar[int]
        from_: str
        to: str
        def __init__(self, from_: _Optional[str] = ..., to: _Optional[str] = ...) -> None: ...
    FLIGHT_FIELD_NUMBER: _ClassVar[int]
    REG_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    VSPEED_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_OF_REG_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    LOGO_ID_FIELD_NUMBER: _ClassVar[int]
    AIRSPACE_FIELD_NUMBER: _ClassVar[int]
    EMS_INFO_FIELD_NUMBER: _ClassVar[int]
    EMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    ICAO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    flight: str
    reg: str
    route: ExtraFlightInfo.Route
    type: str
    squawk: int
    vspeed: int
    age: str
    country_of_reg: int
    schedule: Schedule
    logo_id: int
    airspace: int
    ems_info: EMSInfo
    ems_availability: EMSAvailability
    icao_address: int
    def __init__(self, flight: _Optional[str] = ..., reg: _Optional[str] = ..., route: _Optional[_Union[ExtraFlightInfo.Route, _Mapping]] = ..., type: _Optional[str] = ..., squawk: _Optional[int] = ..., vspeed: _Optional[int] = ..., age: _Optional[str] = ..., country_of_reg: _Optional[int] = ..., schedule: _Optional[_Union[Schedule, _Mapping]] = ..., logo_id: _Optional[int] = ..., airspace: _Optional[int] = ..., ems_info: _Optional[_Union[EMSInfo, _Mapping]] = ..., ems_availability: _Optional[_Union[EMSAvailability, _Mapping]] = ..., icao_address: _Optional[int] = ...) -> None: ...

class SourceStats(_message.Message):
    __slots__ = ("source", "count")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    source: DataSource
    count: int
    def __init__(self, source: _Optional[_Union[DataSource, str]] = ..., count: _Optional[int] = ...) -> None: ...

class Stats(_message.Message):
    __slots__ = ("sources",)
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[SourceStats]
    def __init__(self, sources: _Optional[_Iterable[_Union[SourceStats, _Mapping]]] = ...) -> None: ...

class Flight(_message.Message):
    __slots__ = ("flightid", "lat", "lon", "track", "alt", "speed", "icon", "status", "timestamp", "on_ground", "callsign", "source", "extra_info")
    FLIGHTID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ON_GROUND_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTRA_INFO_FIELD_NUMBER: _ClassVar[int]
    flightid: int
    lat: float
    lon: float
    track: int
    alt: int
    speed: int
    icon: Icon
    status: Status
    timestamp: int
    on_ground: bool
    callsign: str
    source: DataSource
    extra_info: ExtraFlightInfo
    def __init__(self, flightid: _Optional[int] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., track: _Optional[int] = ..., alt: _Optional[int] = ..., speed: _Optional[int] = ..., icon: _Optional[_Union[Icon, str]] = ..., status: _Optional[_Union[Status, str]] = ..., timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ..., extra_info: _Optional[_Union[ExtraFlightInfo, _Mapping]] = ...) -> None: ...

class LiveFeedResponse(_message.Message):
    __slots__ = ("flights_list", "stats", "selected_flight_info")
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    SELECTED_FLIGHT_INFO_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[Flight]
    stats: Stats
    selected_flight_info: _containers.RepeatedCompositeFieldContainer[Flight]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[Flight, _Mapping]]] = ..., stats: _Optional[_Union[Stats, _Mapping]] = ..., selected_flight_info: _Optional[_Iterable[_Union[Flight, _Mapping]]] = ...) -> None: ...

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

class AircraftInfo(_message.Message):
    __slots__ = ("icao_address", "reg", "country_of_reg", "type", "icon", "full_description", "msn", "service", "ac_birth_date", "ac_age_text", "images_list", "is_test_flight", "msn_available", "age_available", "registered_owners")
    ICAO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REG_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_OF_REG_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ICON_FIELD_NUMBER: _ClassVar[int]
    FULL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MSN_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    AC_BIRTH_DATE_FIELD_NUMBER: _ClassVar[int]
    AC_AGE_TEXT_FIELD_NUMBER: _ClassVar[int]
    IMAGES_LIST_FIELD_NUMBER: _ClassVar[int]
    IS_TEST_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    MSN_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    AGE_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    REGISTERED_OWNERS_FIELD_NUMBER: _ClassVar[int]
    icao_address: int
    reg: int
    country_of_reg: int
    type: str
    icon: Icon
    full_description: str
    msn: str
    service: Service
    ac_birth_date: str
    ac_age_text: str
    images_list: _containers.RepeatedCompositeFieldContainer[ImageInfo]
    is_test_flight: bool
    msn_available: bool
    age_available: bool
    registered_owners: str
    def __init__(self, icao_address: _Optional[int] = ..., reg: _Optional[int] = ..., country_of_reg: _Optional[int] = ..., type: _Optional[str] = ..., icon: _Optional[_Union[Icon, str]] = ..., full_description: _Optional[str] = ..., msn: _Optional[str] = ..., service: _Optional[_Union[Service, str]] = ..., ac_birth_date: _Optional[str] = ..., ac_age_text: _Optional[str] = ..., images_list: _Optional[_Iterable[_Union[ImageInfo, _Mapping]]] = ..., is_test_flight: bool = ..., msn_available: bool = ..., age_available: bool = ..., registered_owners: _Optional[str] = ...) -> None: ...

class AltArrival(_message.Message):
    __slots__ = ("arrival", "length")
    ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    arrival: Fix
    length: float
    def __init__(self, arrival: _Optional[_Union[Fix, _Mapping]] = ..., length: _Optional[float] = ...) -> None: ...

class Coordinate(_message.Message):
    __slots__ = ("code", "point")
    CODE_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    code: str
    point: Point
    def __init__(self, code: _Optional[str] = ..., point: _Optional[_Union[Point, _Mapping]] = ...) -> None: ...

class Duration(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class ExtendedFlightInfo(_message.Message):
    __slots__ = ("timestamp", "on_ground", "callsign", "vspeed_availability", "vspeed")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ON_GROUND_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    VSPEED_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    VSPEED_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    on_ground: bool
    callsign: str
    vspeed_availability: bool
    vspeed: int
    def __init__(self, timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., vspeed_availability: bool = ..., vspeed: _Optional[int] = ...) -> None: ...

class FetchSearchIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FetchSearchIndexResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Fix(_message.Message):
    __slots__ = ("coordinate",)
    COORDINATE_FIELD_NUMBER: _ClassVar[int]
    coordinate: Coordinate
    def __init__(self, coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...) -> None: ...

class FlightPlan(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FlightProgress(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FlightSearchData(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FollowFlightRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FollowFlightResponse(_message.Message):
    __slots__ = ("aircraft_info", "flight_plan", "schedule_info", "flight_progress", "flight_info", "flight_trail_list")
    AIRCRAFT_INFO_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_PLAN_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_INFO_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_INFO_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_TRAIL_LIST_FIELD_NUMBER: _ClassVar[int]
    aircraft_info: AircraftInfo
    flight_plan: FlightPlan
    schedule_info: ScheduleInfo
    flight_progress: FlightProgress
    flight_info: ExtendedFlightInfo
    flight_trail_list: _containers.RepeatedCompositeFieldContainer[TrailPoint]
    def __init__(self, aircraft_info: _Optional[_Union[AircraftInfo, _Mapping]] = ..., flight_plan: _Optional[_Union[FlightPlan, _Mapping]] = ..., schedule_info: _Optional[_Union[ScheduleInfo, _Mapping]] = ..., flight_progress: _Optional[_Union[FlightProgress, _Mapping]] = ..., flight_info: _Optional[_Union[ExtendedFlightInfo, _Mapping]] = ..., flight_trail_list: _Optional[_Iterable[_Union[TrailPoint, _Mapping]]] = ...) -> None: ...

class FollowedFlight(_message.Message):
    __slots__ = ("flight_number", "callsign", "from_iata", "from_city", "to_iata", "to_city", "type", "full_description")
    FLIGHT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    FROM_IATA_FIELD_NUMBER: _ClassVar[int]
    FROM_CITY_FIELD_NUMBER: _ClassVar[int]
    TO_IATA_FIELD_NUMBER: _ClassVar[int]
    TO_CITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FULL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    flight_number: str
    callsign: str
    from_iata: str
    from_city: str
    to_iata: str
    to_city: str
    type: str
    full_description: str
    def __init__(self, flight_number: _Optional[str] = ..., callsign: _Optional[str] = ..., from_iata: _Optional[str] = ..., from_city: _Optional[str] = ..., to_iata: _Optional[str] = ..., to_city: _Optional[str] = ..., type: _Optional[str] = ..., full_description: _Optional[str] = ...) -> None: ...

class Geolocation(_message.Message):
    __slots__ = ("lat", "lon")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ...) -> None: ...

class ImageInfo(_message.Message):
    __slots__ = ("url", "copyright", "thumbnail", "medium", "large")
    URL_FIELD_NUMBER: _ClassVar[int]
    COPYRIGHT_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    MEDIUM_FIELD_NUMBER: _ClassVar[int]
    LARGE_FIELD_NUMBER: _ClassVar[int]
    url: str
    copyright: str
    thumbnail: str
    medium: str
    large: str
    def __init__(self, url: _Optional[str] = ..., copyright: _Optional[str] = ..., thumbnail: _Optional[str] = ..., medium: _Optional[str] = ..., large: _Optional[str] = ...) -> None: ...

class Interval(_message.Message):
    __slots__ = ("min", "max")
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: int
    max: int
    def __init__(self, min: _Optional[int] = ..., max: _Optional[int] = ...) -> None: ...

class LiveFlightStatusData(_message.Message):
    __slots__ = ("lat", "lon", "squawk")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    squawk: int
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ..., squawk: _Optional[int] = ...) -> None: ...

class LiveFlightsStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LiveFlightsStatusResponse(_message.Message):
    __slots__ = ("flights_map",)
    FLIGHTS_MAP_FIELD_NUMBER: _ClassVar[int]
    flights_map: LiveFlightStatusData
    def __init__(self, flights_map: _Optional[_Union[LiveFlightStatusData, _Mapping]] = ...) -> None: ...

class LiveTrailRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LiveTrailResponse(_message.Message):
    __slots__ = ("radar_records_list",)
    RADAR_RECORDS_LIST_FIELD_NUMBER: _ClassVar[int]
    radar_records_list: _containers.RepeatedCompositeFieldContainer[RadarHistoryRecord]
    def __init__(self, radar_records_list: _Optional[_Iterable[_Union[RadarHistoryRecord, _Mapping]]] = ...) -> None: ...

class NearbyFlight(_message.Message):
    __slots__ = ("flight", "distance")
    FLIGHT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    flight: Flight
    distance: int
    def __init__(self, flight: _Optional[_Union[Flight, _Mapping]] = ..., distance: _Optional[int] = ...) -> None: ...

class NearestFlightsRequest(_message.Message):
    __slots__ = ("radius",)
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    radius: int
    def __init__(self, radius: _Optional[int] = ...) -> None: ...

class NearestFlightsResponse(_message.Message):
    __slots__ = ("flights_list",)
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[NearbyFlight]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[NearbyFlight, _Mapping]]] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RadarHistoryRecord(_message.Message):
    __slots__ = ("timestamp",)
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    def __init__(self, timestamp: _Optional[int] = ...) -> None: ...

class Route(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ScheduleInfo(_message.Message):
    __slots__ = ("flight_number", "operated_by_id", "scheduled_departure", "scheduled_arrival", "actual_arrival", "arr_terminal", "arr_gate", "baggage_belt")
    FLIGHT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OPERATED_BY_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ARR_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    ARR_GATE_FIELD_NUMBER: _ClassVar[int]
    BAGGAGE_BELT_FIELD_NUMBER: _ClassVar[int]
    flight_number: str
    operated_by_id: int
    scheduled_departure: int
    scheduled_arrival: int
    actual_arrival: int
    arr_terminal: str
    arr_gate: str
    baggage_belt: str
    def __init__(self, flight_number: _Optional[str] = ..., operated_by_id: _Optional[int] = ..., scheduled_departure: _Optional[int] = ..., scheduled_arrival: _Optional[int] = ..., actual_arrival: _Optional[int] = ..., arr_terminal: _Optional[str] = ..., arr_gate: _Optional[str] = ..., baggage_belt: _Optional[str] = ...) -> None: ...

class Tick(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TopFlightsRequest(_message.Message):
    __slots__ = ("limit",)
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    def __init__(self, limit: _Optional[int] = ...) -> None: ...

class TopFlightsResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TrailPoint(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
