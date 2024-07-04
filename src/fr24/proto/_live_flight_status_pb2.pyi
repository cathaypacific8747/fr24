from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LiveFlightStatusData(_message.Message):
    __slots__ = ("lat", "lon", "status", "squawk")
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    lat: float
    lon: float
    status: __common_pb2.Status
    squawk: int
    def __init__(self, lat: _Optional[float] = ..., lon: _Optional[float] = ..., status: _Optional[_Union[__common_pb2.Status, str]] = ..., squawk: _Optional[int] = ...) -> None: ...

class LiveFlightsStatusRequest(_message.Message):
    __slots__ = ("flight_ids_list",)
    FLIGHT_IDS_LIST_FIELD_NUMBER: _ClassVar[int]
    flight_ids_list: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, flight_ids_list: _Optional[_Iterable[int]] = ...) -> None: ...

class LiveFlightsStatusResponse(_message.Message):
    __slots__ = ("flights_map",)
    FLIGHTS_MAP_FIELD_NUMBER: _ClassVar[int]
    flights_map: LiveFlightStatusData
    def __init__(self, flights_map: _Optional[_Union[LiveFlightStatusData, _Mapping]] = ...) -> None: ...
