from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlightStage(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[FlightStage]
    ON_GROUND: _ClassVar[FlightStage]
    TAKING_OFF: _ClassVar[FlightStage]
    AIRBORNE: _ClassVar[FlightStage]
    ON_APPROACH: _ClassVar[FlightStage]

class DelayStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    GRAY: _ClassVar[DelayStatus]
    GREEN: _ClassVar[DelayStatus]
    YELLOW: _ClassVar[DelayStatus]
    RED: _ClassVar[DelayStatus]
UNKNOWN: FlightStage
ON_GROUND: FlightStage
TAKING_OFF: FlightStage
AIRBORNE: FlightStage
ON_APPROACH: FlightStage
GRAY: DelayStatus
GREEN: DelayStatus
YELLOW: DelayStatus
RED: DelayStatus

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
    icon: __common_pb2.Icon
    full_description: str
    msn: str
    service: __common_pb2.Service
    ac_birth_date: str
    ac_age_text: str
    images_list: _containers.RepeatedCompositeFieldContainer[ImageInfo]
    is_test_flight: bool
    msn_available: bool
    age_available: bool
    registered_owners: str
    def __init__(self, icao_address: _Optional[int] = ..., reg: _Optional[int] = ..., country_of_reg: _Optional[int] = ..., type: _Optional[str] = ..., icon: _Optional[_Union[__common_pb2.Icon, str]] = ..., full_description: _Optional[str] = ..., msn: _Optional[str] = ..., service: _Optional[_Union[__common_pb2.Service, str]] = ..., ac_birth_date: _Optional[str] = ..., ac_age_text: _Optional[str] = ..., images_list: _Optional[_Iterable[_Union[ImageInfo, _Mapping]]] = ..., is_test_flight: bool = ..., msn_available: bool = ..., age_available: bool = ..., registered_owners: _Optional[str] = ...) -> None: ...

class Point(_message.Message):
    __slots__ = ("latitude", "longitude")
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    latitude: int
    longitude: int
    def __init__(self, latitude: _Optional[int] = ..., longitude: _Optional[int] = ...) -> None: ...

class Coordinate(_message.Message):
    __slots__ = ("code", "point")
    CODE_FIELD_NUMBER: _ClassVar[int]
    POINT_FIELD_NUMBER: _ClassVar[int]
    code: str
    point: Point
    def __init__(self, code: _Optional[str] = ..., point: _Optional[_Union[Point, _Mapping]] = ...) -> None: ...

class Fix(_message.Message):
    __slots__ = ("airport", "area", "coordinate")
    AIRPORT_FIELD_NUMBER: _ClassVar[int]
    AREA_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_FIELD_NUMBER: _ClassVar[int]
    airport: str
    area: str
    coordinate: Coordinate
    def __init__(self, airport: _Optional[str] = ..., area: _Optional[str] = ..., coordinate: _Optional[_Union[Coordinate, _Mapping]] = ...) -> None: ...

class AltArrival(_message.Message):
    __slots__ = ("arrival", "length")
    ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    arrival: Fix
    length: float
    def __init__(self, arrival: _Optional[_Union[Fix, _Mapping]] = ..., length: _Optional[float] = ...) -> None: ...

class FlightPlan(_message.Message):
    __slots__ = ("departure", "destination", "flight_plan_icao", "length", "alt_arrival_1", "alt_arrival_2", "waypoints_list")
    DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_PLAN_ICAO_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    ALT_ARRIVAL_1_FIELD_NUMBER: _ClassVar[int]
    ALT_ARRIVAL_2_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_LIST_FIELD_NUMBER: _ClassVar[int]
    departure: str
    destination: str
    flight_plan_icao: str
    length: float
    alt_arrival_1: AltArrival
    alt_arrival_2: AltArrival
    waypoints_list: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, departure: _Optional[str] = ..., destination: _Optional[str] = ..., flight_plan_icao: _Optional[str] = ..., length: _Optional[float] = ..., alt_arrival_1: _Optional[_Union[AltArrival, _Mapping]] = ..., alt_arrival_2: _Optional[_Union[AltArrival, _Mapping]] = ..., waypoints_list: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...) -> None: ...

class ScheduleInfo(_message.Message):
    __slots__ = ("flight_number", "operated_by_id", "painted_as_id", "origin_id", "destination_id", "diverted_to_id", "scheduled_departure", "scheduled_arrival", "actual_departure", "actual_arrival", "arr_terminal", "arr_gate", "baggage_belt")
    FLIGHT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    OPERATED_BY_ID_FIELD_NUMBER: _ClassVar[int]
    PAINTED_AS_ID_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_ID_FIELD_NUMBER: _ClassVar[int]
    DESTINATION_ID_FIELD_NUMBER: _ClassVar[int]
    DIVERTED_TO_ID_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    SCHEDULED_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_DEPARTURE_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_ARRIVAL_FIELD_NUMBER: _ClassVar[int]
    ARR_TERMINAL_FIELD_NUMBER: _ClassVar[int]
    ARR_GATE_FIELD_NUMBER: _ClassVar[int]
    BAGGAGE_BELT_FIELD_NUMBER: _ClassVar[int]
    flight_number: str
    operated_by_id: int
    painted_as_id: int
    origin_id: int
    destination_id: int
    diverted_to_id: int
    scheduled_departure: int
    scheduled_arrival: int
    actual_departure: int
    actual_arrival: int
    arr_terminal: str
    arr_gate: str
    baggage_belt: str
    def __init__(self, flight_number: _Optional[str] = ..., operated_by_id: _Optional[int] = ..., painted_as_id: _Optional[int] = ..., origin_id: _Optional[int] = ..., destination_id: _Optional[int] = ..., diverted_to_id: _Optional[int] = ..., scheduled_departure: _Optional[int] = ..., scheduled_arrival: _Optional[int] = ..., actual_departure: _Optional[int] = ..., actual_arrival: _Optional[int] = ..., arr_terminal: _Optional[str] = ..., arr_gate: _Optional[str] = ..., baggage_belt: _Optional[str] = ...) -> None: ...

class FlightProgress(_message.Message):
    __slots__ = ("traversed_distance", "remaining_distance", "elapsed_time", "remaining_time", "eta", "great_circle_distance", "mean_flight_time", "flight_stage", "delay_status")
    TRAVERSED_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REMAINING_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ELAPSED_TIME_FIELD_NUMBER: _ClassVar[int]
    REMAINING_TIME_FIELD_NUMBER: _ClassVar[int]
    ETA_FIELD_NUMBER: _ClassVar[int]
    GREAT_CIRCLE_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MEAN_FLIGHT_TIME_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_STAGE_FIELD_NUMBER: _ClassVar[int]
    DELAY_STATUS_FIELD_NUMBER: _ClassVar[int]
    traversed_distance: int
    remaining_distance: int
    elapsed_time: int
    remaining_time: int
    eta: int
    great_circle_distance: int
    mean_flight_time: int
    flight_stage: FlightStage
    delay_status: DelayStatus
    def __init__(self, traversed_distance: _Optional[int] = ..., remaining_distance: _Optional[int] = ..., elapsed_time: _Optional[int] = ..., remaining_time: _Optional[int] = ..., eta: _Optional[int] = ..., great_circle_distance: _Optional[int] = ..., mean_flight_time: _Optional[int] = ..., flight_stage: _Optional[_Union[FlightStage, str]] = ..., delay_status: _Optional[_Union[DelayStatus, str]] = ...) -> None: ...

class FollowFlightRequest(_message.Message):
    __slots__ = ("flight_id", "restriction_mode")
    FLIGHT_ID_FIELD_NUMBER: _ClassVar[int]
    RESTRICTION_MODE_FIELD_NUMBER: _ClassVar[int]
    flight_id: int
    restriction_mode: __common_pb2.RestrictionVisibility
    def __init__(self, flight_id: _Optional[int] = ..., restriction_mode: _Optional[_Union[__common_pb2.RestrictionVisibility, str]] = ...) -> None: ...

class ExtendedFlightInfo(_message.Message):
    __slots__ = ("flightid", "lat", "lon", "track", "alt", "speed", "status", "timestamp", "on_ground", "callsign", "source", "ems_availability", "ems_info", "squawk_availability", "squawk", "vspeed_availability", "vspeed", "airspace_availability", "airspace")
    FLIGHTID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ON_GROUND_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    EMS_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    EMS_INFO_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    VSPEED_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    VSPEED_FIELD_NUMBER: _ClassVar[int]
    AIRSPACE_AVAILABILITY_FIELD_NUMBER: _ClassVar[int]
    AIRSPACE_FIELD_NUMBER: _ClassVar[int]
    flightid: int
    lat: float
    lon: float
    track: int
    alt: int
    speed: int
    status: __common_pb2.Status
    timestamp: int
    on_ground: bool
    callsign: str
    source: __common_pb2.DataSource
    ems_availability: __common_pb2.EMSAvailability
    ems_info: __common_pb2.EMSInfo
    squawk_availability: bool
    squawk: int
    vspeed_availability: bool
    vspeed: int
    airspace_availability: bool
    airspace: str
    def __init__(self, flightid: _Optional[int] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., track: _Optional[int] = ..., alt: _Optional[int] = ..., speed: _Optional[int] = ..., status: _Optional[_Union[__common_pb2.Status, str]] = ..., timestamp: _Optional[int] = ..., on_ground: bool = ..., callsign: _Optional[str] = ..., source: _Optional[_Union[__common_pb2.DataSource, str]] = ..., ems_availability: _Optional[_Union[__common_pb2.EMSAvailability, _Mapping]] = ..., ems_info: _Optional[_Union[__common_pb2.EMSInfo, _Mapping]] = ..., squawk_availability: bool = ..., squawk: _Optional[int] = ..., vspeed_availability: bool = ..., vspeed: _Optional[int] = ..., airspace_availability: bool = ..., airspace: _Optional[str] = ...) -> None: ...

class TrailPoint(_message.Message):
    __slots__ = ("snapshot_id", "lat", "lon", "altitude", "spd", "heading", "vspd")
    SNAPSHOT_ID_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    SPD_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    VSPD_FIELD_NUMBER: _ClassVar[int]
    snapshot_id: int
    lat: float
    lon: float
    altitude: int
    spd: int
    heading: int
    vspd: int
    def __init__(self, snapshot_id: _Optional[int] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., altitude: _Optional[int] = ..., spd: _Optional[int] = ..., heading: _Optional[int] = ..., vspd: _Optional[int] = ...) -> None: ...

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
