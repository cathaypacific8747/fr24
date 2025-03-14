"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from builtins import (
    bool,
    float,
    int,
)
from collections.abc import (
    Iterable,
)
from fr24.proto._common_pb2 import (
    Flight,
)
from google.protobuf.descriptor import (
    Descriptor,
    FileDescriptor,
)
from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer,
)
from google.protobuf.message import (
    Message,
)
from typing import (
    Literal,
    final,
)

DESCRIPTOR: FileDescriptor

@final
class Geolocation(Message):
    DESCRIPTOR: Descriptor

    LAT_FIELD_NUMBER: int
    LON_FIELD_NUMBER: int
    lat: float
    """Latitude, degrees, -90 to 90"""
    lon: float
    """Longitude, degrees, -180 to 180"""
    def __init__(
        self,
        *,
        lat: float = ...,
        lon: float = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["lat", b"lat", "lon", b"lon"]) -> None: ...

@final
class NearestFlightsRequest(Message):
    DESCRIPTOR: Descriptor

    LOCATION_FIELD_NUMBER: int
    RADIUS_FIELD_NUMBER: int
    LIMIT_FIELD_NUMBER: int
    radius: int
    """Radius, metres"""
    limit: int
    """Maximum number of aircraft to return"""
    @property
    def location(self) -> Geolocation: ...
    def __init__(
        self,
        *,
        location: Geolocation | None = ...,
        radius: int = ...,
        limit: int = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["location", b"location"]) -> bool: ...
    def ClearField(self, field_name: Literal["limit", b"limit", "location", b"location", "radius", b"radius"]) -> None: ...

@final
class NearbyFlight(Message):
    DESCRIPTOR: Descriptor

    FLIGHT_FIELD_NUMBER: int
    DISTANCE_FIELD_NUMBER: int
    distance: int
    """Distance from the location, metres"""
    @property
    def flight(self) -> Flight: ...
    def __init__(
        self,
        *,
        flight: Flight | None = ...,
        distance: int = ...,
    ) -> None: ...
    def HasField(self, field_name: Literal["flight", b"flight"]) -> bool: ...
    def ClearField(self, field_name: Literal["distance", b"distance", "flight", b"flight"]) -> None: ...

@final
class NearestFlightsResponse(Message):
    DESCRIPTOR: Descriptor

    FLIGHTS_LIST_FIELD_NUMBER: int
    @property
    def flights_list(self) -> RepeatedCompositeFieldContainer[NearbyFlight]: ...
    def __init__(
        self,
        *,
        flights_list: Iterable[NearbyFlight] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["flights_list", b"flights_list"]) -> None: ...
