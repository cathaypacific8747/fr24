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

class Route(_message.Message):
    __slots__ = ("to", "diverted_to")
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    DIVERTED_TO_FIELD_NUMBER: _ClassVar[int]
    to: str
    diverted_to: str
    def __init__(self, to: _Optional[str] = ..., diverted_to: _Optional[str] = ..., **kwargs) -> None: ...

class ExtraFlightInfo(_message.Message):
    __slots__ = ("flight", "reg", "route", "type", "squawk", "vspeed", "age", "country_of_reg", "schedule", "logo_id", "airspace", "ems_info", "ems_availability", "icao_address", "operated_by_id", "squawk_availability", "vspeed_availability", "airspace_availability", "airspace_id")
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
    OPERATED_BY_ID_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    VSPEED_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    AIRSPACE_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    AIRSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    flight: str
    reg: str
    route: Route
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
    operated_by_id: int
    squawk_availability: bool
    vspeed_availability: bool
    airspace_availability: bool
    airspace_id: str
    def __init__(self, flight: _Optional[str] = ..., reg: _Optional[str] = ..., route: _Optional[_Union[Route, _Mapping]] = ..., type: _Optional[str] = ..., squawk: _Optional[int] = ..., vspeed: _Optional[int] = ..., age: _Optional[str] = ..., country_of_reg: _Optional[int] = ..., schedule: _Optional[_Union[Schedule, _Mapping]] = ..., logo_id: _Optional[int] = ..., airspace: _Optional[int] = ..., ems_info: _Optional[_Union[EMSInfo, _Mapping]] = ..., ems_availability: _Optional[_Union[EMSAvailability, _Mapping]] = ..., icao_address: _Optional[int] = ..., operated_by_id: _Optional[int] = ..., squawk_availability: bool = ..., vspeed_availability: bool = ..., airspace_availability: bool = ..., airspace_id: _Optional[str] = ...) -> None: ...

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

class Duration(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class Tick(_message.Message):
    __slots__ = ("count",)
    COUNT_FIELD_NUMBER: _ClassVar[int]
    count: int
    def __init__(self, count: _Optional[int] = ...) -> None: ...

class RadarHistoryRecord(_message.Message):
    __slots__ = ("timestamp", "lat", "lon", "altitude", "spd", "heading", "vspd", "squawk", "source", "callsign")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SPD_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    VSPD_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    lat: float
    lon: float
    altitude: int
    spd: int
    heading: int
    vspd: int
    squawk: int
    source: DataSource
    callsign: str
    def __init__(self, timestamp: _Optional[int] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., altitude: _Optional[int] = ..., spd: _Optional[int] = ..., heading: _Optional[int] = ..., vspd: _Optional[int] = ..., squawk: _Optional[int] = ..., source: _Optional[_Union[DataSource, str]] = ..., callsign: _Optional[str] = ...) -> None: ...
