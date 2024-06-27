from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Geolocation(_message.Message):
    __slots__ = ("lat", "lon")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ...) -> None: ...

class NearestFlightsRequest(_message.Message):
    __slots__ = ("location", "radius", "limit")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    location: Geolocation
    radius: int
    limit: int
    def __init__(self, location: _Optional[_Union[Geolocation, _Mapping]] = ..., radius: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class NearbyFlight(_message.Message):
    __slots__ = ("flight", "distance")
    FLIGHT_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    flight: __common_pb2.Flight
    distance: int
    def __init__(self, flight: _Optional[_Union[__common_pb2.Flight, _Mapping]] = ..., distance: _Optional[int] = ...) -> None: ...

class NearestFlightsResponse(_message.Message):
    __slots__ = ("flights_list",)
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[NearbyFlight]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[NearbyFlight, _Mapping]]] = ...) -> None: ...
