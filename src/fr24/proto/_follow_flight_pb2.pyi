"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

import sys

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions
from builtins import (
    bool,
    float,
    int,
    str,
    type,
)
from collections.abc import (
    Iterable,
)
from fr24.proto._common_pb2 import (
    DataSource,
    EMSAvailability,
    EMSInfo,
    Icon,
    RestrictionVisibility,
    Service,
    Status,
)
from google.protobuf.descriptor import (
    Descriptor,
    EnumDescriptor,
    FileDescriptor,
)
from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
)
from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper,
)
from google.protobuf.message import (
    Message,
)
from typing import (
    Literal,
    NewType,
    final,
)

DESCRIPTOR: FileDescriptor

class _FlightStage:
    ValueType = NewType("ValueType", int)
    V: typing_extensions.TypeAlias = ValueType

class _FlightStageEnumTypeWrapper(_EnumTypeWrapper[_FlightStage.ValueType], type):
    DESCRIPTOR: EnumDescriptor
    UNKNOWN: _FlightStage.ValueType  # 0
    ON_GROUND: _FlightStage.ValueType  # 1
    ASCENDING: _FlightStage.ValueType  # 2
    AIRBORNE: _FlightStage.ValueType  # 3
    DESCENDING: _FlightStage.ValueType  # 4
    DIVERSION: _FlightStage.ValueType  # 5

class FlightStage(_FlightStage, metaclass=_FlightStageEnumTypeWrapper): ...

UNKNOWN: FlightStage.ValueType  # 0
ON_GROUND: FlightStage.ValueType  # 1
ASCENDING: FlightStage.ValueType  # 2
AIRBORNE: FlightStage.ValueType  # 3
DESCENDING: FlightStage.ValueType  # 4
DIVERSION: FlightStage.ValueType  # 5

class _DelayStatus:
    ValueType = NewType("ValueType", int)
    V: typing_extensions.TypeAlias = ValueType

class _DelayStatusEnumTypeWrapper(_EnumTypeWrapper[_DelayStatus.ValueType], type):
    DESCRIPTOR: EnumDescriptor
    GRAY: _DelayStatus.ValueType  # 0
    GREEN: _DelayStatus.ValueType  # 1
    YELLOW: _DelayStatus.ValueType  # 2
    RED: _DelayStatus.ValueType  # 3

class DelayStatus(_DelayStatus, metaclass=_DelayStatusEnumTypeWrapper): ...

GRAY: DelayStatus.ValueType  # 0
GREEN: DelayStatus.ValueType  # 1
YELLOW: DelayStatus.ValueType  # 2
RED: DelayStatus.ValueType  # 3

@final
class ImageInfo(Message):
    DESCRIPTOR: Descriptor

    URL_FIELD_NUMBER: int
    COPYRIGHT_FIELD_NUMBER: int
    THUMBNAIL_FIELD_NUMBER: int
    MEDIUM_FIELD_NUMBER: int
    LARGE_FIELD_NUMBER: int
    SIDEVIEW_FIELD_NUMBER: int
    url: str
    """Image URL"""
    copyright: str
    """Copyright information (e.g. `"R Skywalker"`)"""
    thumbnail: str
    """URL for thumbnail image (e.g. `"https://cdn.jetphotos.com/200/5/459674_1738674373_tb.jpg"`)"""
    medium: str
    """URL for medium-sized image (e.g. `"https://cdn.jetphotos.com/400/5/459674_1738674373.jpg"`)"""
    large: str
    """URL for large-sized image (e.g. `"https://cdn.jetphotos.com/640/5/459674_1738674373.jpg"`)"""
    sideview: str
    def __init__(
        self,
        *,
        url: str = ...,
        copyright: str = ...,
        thumbnail: str = ...,
        medium: str = ...,
        large: str = ...,
        sideview: str = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["copyright", b"copyright", "large", b"large", "medium", b"medium", "sideview", b"sideview", "thumbnail", b"thumbnail", "url", b"url"]) -> None: ...

@final
class AircraftInfo(Message):
    DESCRIPTOR: Descriptor

    ICAO_ADDRESS_FIELD_NUMBER: int
    REG_FIELD_NUMBER: int
    COUNTRY_OF_REG_FIELD_NUMBER: int
    TYPE_FIELD_NUMBER: int
    ICON_FIELD_NUMBER: int
    FULL_DESCRIPTION_FIELD_NUMBER: int
    MSN_FIELD_NUMBER: int
    SERVICE_FIELD_NUMBER: int
    AC_BIRTH_DATE_FIELD_NUMBER: int
    AC_AGE_TEXT_FIELD_NUMBER: int
    IMAGES_LIST_FIELD_NUMBER: int
    IS_TEST_FLIGHT_FIELD_NUMBER: int
    MSN_AVAILABLE_FIELD_NUMBER: int
    AGE_AVAILABLE_FIELD_NUMBER: int
    REGISTERED_OWNERS_FIELD_NUMBER: int
    IS_COUNTRY_OF_REG_AVAILABLE_FIELD_NUMBER: int
    icao_address: int
    """ICAO 24-bit address of the aircraft (e.g. `3789483`)"""
    reg: int
    """Registration number (e.g. `7867035`)"""
    country_of_reg: int
    """Country of registration code (e.g. `3`)"""
    type: str
    """Aircraft type code (e.g. `"A359"`)"""
    icon: Icon.ValueType
    full_description: str
    """Full aircraft description (e.g. `"Airbus A350-941"`)"""
    msn: str
    service: Service.ValueType
    ac_birth_date: str
    """Aircraft birth date string (e.g. `"2017-06-28"`)"""
    ac_age_text: str
    """Aircraft age (e.g. `"7 years old"`)"""
    is_test_flight: bool
    msn_available: bool
    age_available: bool
    registered_owners: str
    """Aircraft owner name (e.g. `"Air France"`)"""
    is_country_of_reg_available: bool
    @property
    def images_list(self) -> RepeatedCompositeFieldContainer[ImageInfo]: ...
    def __init__(
        self,
        *,
        icao_address: int = ...,
        reg: int = ...,
        country_of_reg: int = ...,
        type: str = ...,
        icon: Icon.ValueType = ...,
        full_description: str = ...,
        msn: str = ...,
        service: Service.ValueType = ...,
        ac_birth_date: str = ...,
        ac_age_text: str = ...,
        images_list: Iterable[ImageInfo] | None = ...,
        is_test_flight: bool = ...,
        msn_available: bool = ...,
        age_available: bool = ...,
        registered_owners: str = ...,
        is_country_of_reg_available: bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["ac_age_text", b"ac_age_text", "ac_birth_date", b"ac_birth_date", "age_available", b"age_available", "country_of_reg", b"country_of_reg", "full_description", b"full_description", "icao_address", b"icao_address", "icon", b"icon", "images_list", b"images_list", "is_country_of_reg_available", b"is_country_of_reg_available", "is_test_flight", b"is_test_flight", "msn", b"msn", "msn_available", b"msn_available", "reg", b"reg", "registered_owners", b"registered_owners", "service", b"service", "type", b"type"]) -> None: ...

@final
class Point(Message):
    DESCRIPTOR: Descriptor

    LATITUDE_FIELD_NUMBER: int
    LONGITUDE_FIELD_NUMBER: int
    latitude: int
    """Latitude, degrees, -90 to 90"""
    longitude: int
    """Longitude, degrees, -180 to 180"""
    def __init__(
        self,
        *,
        latitude: int = ...,
        longitude: int = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["latitude", b"latitude", "longitude", b"longitude"]) -> None: ...

@final
class Coordinate(Message):
    DESCRIPTOR: Descriptor

    CODE_FIELD_NUMBER: int
    POINT_FIELD_NUMBER: int
    code: str
    @property
    def point(self) -> Point: ...
    def __init__(
        self,
        *,
        code: str = ...,
        point: Point | None = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["point", b"point"]) -> bool: ...
    def ClearField(self, field_name: Literal["code", b"code", "point", b"point"]) -> None: ...

@final
class Fix(Message):
    DESCRIPTOR: Descriptor

    AIRPORT_FIELD_NUMBER: int
    AREA_FIELD_NUMBER: int
    COORDINATE_FIELD_NUMBER: int
    airport: str
    area: str
    @property
    def coordinate(self) -> Coordinate: ...
    def __init__(
        self,
        *,
        airport: str = ...,
        area: str = ...,
        coordinate: Coordinate | None = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["coordinate", b"coordinate"]) -> bool: ...
    def ClearField(self, field_name: Literal["airport", b"airport", "area", b"area", "coordinate", b"coordinate"]) -> None: ...

@final
class AltArrival(Message):
    DESCRIPTOR: Descriptor

    ARRIVAL_FIELD_NUMBER: int
    LENGTH_FIELD_NUMBER: int
    length: float
    @property
    def arrival(self) -> Fix: ...
    def __init__(
        self,
        *,
        arrival: Fix | None = ...,
        length: float = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["arrival", b"arrival"]) -> bool: ...
    def ClearField(self, field_name: Literal["arrival", b"arrival", "length", b"length"]) -> None: ...

@final
class FlightPlan(Message):
    DESCRIPTOR: Descriptor

    DEPARTURE_FIELD_NUMBER: int
    DESTINATION_FIELD_NUMBER: int
    FLIGHT_PLAN_ICAO_FIELD_NUMBER: int
    LENGTH_FIELD_NUMBER: int
    ALT_ARRIVAL_1_FIELD_NUMBER: int
    ALT_ARRIVAL_2_FIELD_NUMBER: int
    WAYPOINTS_LIST_FIELD_NUMBER: int
    departure: str
    destination: str
    flight_plan_icao: str
    length: float
    @property
    def alt_arrival_1(self) -> AltArrival: ...
    @property
    def alt_arrival_2(self) -> AltArrival: ...
    @property
    def waypoints_list(self) -> RepeatedCompositeFieldContainer[Point]: ...
    def __init__(
        self,
        *,
        departure: str = ...,
        destination: str = ...,
        flight_plan_icao: str = ...,
        length: float = ...,
        alt_arrival_1: AltArrival | None = ...,
        alt_arrival_2: AltArrival | None = ...,
        waypoints_list: Iterable[Point] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["alt_arrival_1", b"alt_arrival_1", "alt_arrival_2", b"alt_arrival_2"]) -> bool: ...
    def ClearField(self, field_name: Literal["alt_arrival_1", b"alt_arrival_1", "alt_arrival_2", b"alt_arrival_2", "departure", b"departure", "destination", b"destination", "flight_plan_icao", b"flight_plan_icao", "length", b"length", "waypoints_list", b"waypoints_list"]) -> None: ...

@final
class ScheduleInfo(Message):
    DESCRIPTOR: Descriptor

    FLIGHT_NUMBER_FIELD_NUMBER: int
    OPERATED_BY_ID_FIELD_NUMBER: int
    PAINTED_AS_ID_FIELD_NUMBER: int
    ORIGIN_ID_FIELD_NUMBER: int
    DESTINATION_ID_FIELD_NUMBER: int
    DIVERTED_TO_ID_FIELD_NUMBER: int
    SCHEDULED_DEPARTURE_FIELD_NUMBER: int
    SCHEDULED_ARRIVAL_FIELD_NUMBER: int
    ACTUAL_DEPARTURE_FIELD_NUMBER: int
    ACTUAL_ARRIVAL_FIELD_NUMBER: int
    ARR_TERMINAL_FIELD_NUMBER: int
    ARR_GATE_FIELD_NUMBER: int
    BAGGAGE_BELT_FIELD_NUMBER: int
    flight_number: str
    """Flight number with airline prefix (e.g. `"AF334"`)"""
    operated_by_id: int
    """ID of the operating airline (e.g. `15`)"""
    painted_as_id: int
    """ID of the airline the aircraft is painted as (e.g. `15`)"""
    origin_id: int
    """Origin airport ID (e.g. `598`)"""
    destination_id: int
    """Destination airport ID (e.g. `451`)"""
    diverted_to_id: int
    """Diverted to airport ID"""
    scheduled_departure: int
    """Scheduled Time of Departure, Unix timestamp in seconds"""
    scheduled_arrival: int
    """Scheduled Time of Arrival, Unix timestamp in seconds"""
    actual_departure: int
    """Actual Time of Departure, Unix timestamp in seconds"""
    actual_arrival: int
    """Actual Time of Arrival, Unix timestamp in seconds"""
    arr_terminal: str
    """Arrival terminal (e.g. `"E"`)"""
    arr_gate: str
    """Arrival gate (e.g. `"E6"`)"""
    baggage_belt: str
    """Baggage belt (e.g. `"4"`)"""
    def __init__(
        self,
        *,
        flight_number: str = ...,
        operated_by_id: int = ...,
        painted_as_id: int = ...,
        origin_id: int = ...,
        destination_id: int = ...,
        diverted_to_id: int = ...,
        scheduled_departure: int = ...,
        scheduled_arrival: int = ...,
        actual_departure: int = ...,
        actual_arrival: int = ...,
        arr_terminal: str = ...,
        arr_gate: str = ...,
        baggage_belt: str = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["actual_arrival", b"actual_arrival", "actual_departure", b"actual_departure", "arr_gate", b"arr_gate", "arr_terminal", b"arr_terminal", "baggage_belt", b"baggage_belt", "destination_id", b"destination_id", "diverted_to_id", b"diverted_to_id", "flight_number", b"flight_number", "operated_by_id", b"operated_by_id", "origin_id", b"origin_id", "painted_as_id", b"painted_as_id", "scheduled_arrival", b"scheduled_arrival", "scheduled_departure", b"scheduled_departure"]) -> None: ...

@final
class FlightProgress(Message):
    DESCRIPTOR: Descriptor

    TRAVERSED_DISTANCE_FIELD_NUMBER: int
    REMAINING_DISTANCE_FIELD_NUMBER: int
    ELAPSED_TIME_FIELD_NUMBER: int
    REMAINING_TIME_FIELD_NUMBER: int
    ETA_FIELD_NUMBER: int
    GREAT_CIRCLE_DISTANCE_FIELD_NUMBER: int
    MEAN_FLIGHT_TIME_FIELD_NUMBER: int
    FLIGHT_STAGE_FIELD_NUMBER: int
    DELAY_STATUS_FIELD_NUMBER: int
    PROGRESS_PCT_FIELD_NUMBER: int
    traversed_distance: int
    """Distance traversed in the flight, meters"""
    remaining_distance: int
    """Remaining distance to destination, meters"""
    elapsed_time: int
    """Elapsed flight time, seconds"""
    remaining_time: int
    """Remaining flight time, seconds"""
    eta: int
    """Estimated Time of Arrival, Unix timestamp in seconds"""
    great_circle_distance: int
    """Great circle distance of the first, meters"""
    mean_flight_time: int
    """Mean flight time for this route, seconds"""
    flight_stage: FlightStage.ValueType
    delay_status: DelayStatus.ValueType
    progress_pct: int
    """Flight progress percentage (e.g. `82`)"""
    def __init__(
        self,
        *,
        traversed_distance: int = ...,
        remaining_distance: int = ...,
        elapsed_time: int = ...,
        remaining_time: int = ...,
        eta: int = ...,
        great_circle_distance: int = ...,
        mean_flight_time: int = ...,
        flight_stage: FlightStage.ValueType = ...,
        delay_status: DelayStatus.ValueType = ...,
        progress_pct: int = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["delay_status", b"delay_status", "elapsed_time", b"elapsed_time", "eta", b"eta", "flight_stage", b"flight_stage", "great_circle_distance", b"great_circle_distance", "mean_flight_time", b"mean_flight_time", "progress_pct", b"progress_pct", "remaining_distance", b"remaining_distance", "remaining_time", b"remaining_time", "traversed_distance", b"traversed_distance"]) -> None: ...

@final
class FollowFlightRequest(Message):
    DESCRIPTOR: Descriptor

    FLIGHT_ID_FIELD_NUMBER: int
    RESTRICTION_MODE_FIELD_NUMBER: int
    flight_id: int
    """FR24 Flight ID (e.g. `962788562` = `0x3962fcd2`)"""
    restriction_mode: RestrictionVisibility.ValueType
    def __init__(
        self,
        *,
        flight_id: int = ...,
        restriction_mode: RestrictionVisibility.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["flight_id", b"flight_id", "restriction_mode", b"restriction_mode"]) -> None: ...

@final
class ExtendedFlightInfo(Message):
    DESCRIPTOR: Descriptor

    FLIGHTID_FIELD_NUMBER: int
    LAT_FIELD_NUMBER: int
    LON_FIELD_NUMBER: int
    TRACK_FIELD_NUMBER: int
    ALT_FIELD_NUMBER: int
    SPEED_FIELD_NUMBER: int
    STATUS_FIELD_NUMBER: int
    TIMESTAMP_MS_FIELD_NUMBER: int
    ON_GROUND_FIELD_NUMBER: int
    CALLSIGN_FIELD_NUMBER: int
    SOURCE_FIELD_NUMBER: int
    EMS_AVAILABILITY_FIELD_NUMBER: int
    EMS_INFO_FIELD_NUMBER: int
    SQUAWK_AVAILABILITY_FIELD_NUMBER: int
    SQUAWK_FIELD_NUMBER: int
    VSPEED_AVAILABILITY_FIELD_NUMBER: int
    VSPEED_FIELD_NUMBER: int
    AIRSPACE_AVAILABILITY_FIELD_NUMBER: int
    AIRSPACE_FIELD_NUMBER: int
    AIRSPACE_ID_FIELD_NUMBER: int
    SERVER_TIME_MS_FIELD_NUMBER: int
    flightid: int
    """Flight ID (e.g. `962788562` = `0x3962fcd2`)"""
    lat: float
    """Latitude, degrees, -90 to 90"""
    lon: float
    """Longitude, degrees, -180 to 180"""
    track: int
    """True track angle, degrees clockwise from North"""
    alt: int
    """Altitude, feet"""
    speed: int
    """Ground Speed, knots"""
    status: Status.ValueType
    timestamp_ms: int
    """Unix timestamp of message, milliseconds (e.g. `1741377144019`)"""
    on_ground: bool
    callsign: str
    """Callsign (e.g. `"AFR334"`)"""
    source: DataSource.ValueType
    squawk_availability: bool
    squawk: int
    """Squawk code, in base-10 (e.g. `3041` = 0o5741)"""
    vspeed_availability: bool
    vspeed: int
    """Vertical speed (e.g. `3328`)"""
    airspace_availability: bool
    airspace: str
    """Airspace, free-form text (e.g. `"Shannon UIR"`)"""
    airspace_id: str
    """Airspace ID (e.g. `"FIR_EINN_U"`)"""
    server_time_ms: int
    """Server timestamp, Unix timestamp in milliseconds (e.g. `1741377145974`)"""
    @property
    def ems_availability(self) -> EMSAvailability: ...
    @property
    def ems_info(self) -> EMSInfo: ...
    def __init__(
        self,
        *,
        flightid: int = ...,
        lat: float = ...,
        lon: float = ...,
        track: int = ...,
        alt: int = ...,
        speed: int = ...,
        status: Status.ValueType = ...,
        timestamp_ms: int = ...,
        on_ground: bool = ...,
        callsign: str = ...,
        source: DataSource.ValueType = ...,
        ems_availability: EMSAvailability | None = ...,
        ems_info: EMSInfo | None = ...,
        squawk_availability: bool = ...,
        squawk: int = ...,
        vspeed_availability: bool = ...,
        vspeed: int = ...,
        airspace_availability: bool = ...,
        airspace: str = ...,
        airspace_id: str = ...,
        server_time_ms: int = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["ems_availability", b"ems_availability", "ems_info", b"ems_info"]) -> bool: ...
    def ClearField(self, field_name: Literal["airspace", b"airspace", "airspace_availability", b"airspace_availability", "airspace_id", b"airspace_id", "alt", b"alt", "callsign", b"callsign", "ems_availability", b"ems_availability", "ems_info", b"ems_info", "flightid", b"flightid", "lat", b"lat", "lon", b"lon", "on_ground", b"on_ground", "server_time_ms", b"server_time_ms", "source", b"source", "speed", b"speed", "squawk", b"squawk", "squawk_availability", b"squawk_availability", "status", b"status", "timestamp_ms", b"timestamp_ms", "track", b"track", "vspeed", b"vspeed", "vspeed_availability", b"vspeed_availability"]) -> None: ...

@final
class TrailPoint(Message):
    DESCRIPTOR: Descriptor

    SNAPSHOT_ID_FIELD_NUMBER: int
    LAT_FIELD_NUMBER: int
    LON_FIELD_NUMBER: int
    ALTITUDE_FIELD_NUMBER: int
    SPD_FIELD_NUMBER: int
    HEADING_FIELD_NUMBER: int
    VSPD_FIELD_NUMBER: int
    snapshot_id: int
    """Snapshot ID, likely Unix timestamp in seconds (e.g. `1741356300`)"""
    lat: float
    """Latitude, degrees, -90 to 90"""
    lon: float
    """Longitude, degrees, -180 to 180"""
    altitude: int
    """Altitude, feet"""
    spd: int
    """Ground speed, knots"""
    heading: int
    """True track angle, degrees clockwise from North.
    Note: despite the name, heading is not transmitted in ADS-B.
    """
    vspd: int
    """Vertical Speed, feet per minute"""
    def __init__(
        self,
        *,
        snapshot_id: int = ...,
        lat: float = ...,
        lon: float = ...,
        altitude: int = ...,
        spd: int = ...,
        heading: int = ...,
        vspd: int = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["altitude", b"altitude", "heading", b"heading", "lat", b"lat", "lon", b"lon", "snapshot_id", b"snapshot_id", "spd", b"spd", "vspd", b"vspd"]) -> None: ...

@final
class FollowFlightResponse(Message):
    DESCRIPTOR: Descriptor

    AIRCRAFT_INFO_FIELD_NUMBER: int
    FLIGHT_PLAN_FIELD_NUMBER: int
    SCHEDULE_INFO_FIELD_NUMBER: int
    FLIGHT_PROGRESS_FIELD_NUMBER: int
    FLIGHT_INFO_FIELD_NUMBER: int
    FLIGHT_TRAIL_LIST_FIELD_NUMBER: int
    @property
    def aircraft_info(self) -> AircraftInfo: ...
    @property
    def flight_plan(self) -> FlightPlan: ...
    @property
    def schedule_info(self) -> ScheduleInfo: ...
    @property
    def flight_progress(self) -> FlightProgress: ...
    @property
    def flight_info(self) -> ExtendedFlightInfo: ...
    @property
    def flight_trail_list(self) -> RepeatedCompositeFieldContainer[TrailPoint]: ...
    def __init__(
        self,
        *,
        aircraft_info: AircraftInfo | None = ...,
        flight_plan: FlightPlan | None = ...,
        schedule_info: ScheduleInfo | None = ...,
        flight_progress: FlightProgress | None = ...,
        flight_info: ExtendedFlightInfo | None = ...,
        flight_trail_list: Iterable[TrailPoint] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["aircraft_info", b"aircraft_info", "flight_info", b"flight_info", "flight_plan", b"flight_plan", "flight_progress", b"flight_progress", "schedule_info", b"schedule_info"]) -> bool: ...
    def ClearField(self, field_name: Literal["aircraft_info", b"aircraft_info", "flight_info", b"flight_info", "flight_plan", b"flight_plan", "flight_progress", b"flight_progress", "flight_trail_list", b"flight_trail_list", "schedule_info", b"schedule_info"]) -> None: ...
