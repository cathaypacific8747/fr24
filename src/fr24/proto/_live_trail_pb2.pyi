from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

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
    source: __common_pb2.DataSource
    callsign: str
    def __init__(self, timestamp: _Optional[int] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., altitude: _Optional[int] = ..., spd: _Optional[int] = ..., heading: _Optional[int] = ..., vspd: _Optional[int] = ..., squawk: _Optional[int] = ..., source: _Optional[_Union[__common_pb2.DataSource, str]] = ..., callsign: _Optional[str] = ...) -> None: ...

class LiveTrailRequest(_message.Message):
    __slots__ = ("flight_id",)
    FLIGHT_ID_FIELD_NUMBER: _ClassVar[int]
    flight_id: int
    def __init__(self, flight_id: _Optional[int] = ...) -> None: ...

class LiveTrailResponse(_message.Message):
    __slots__ = ("radar_records_list",)
    RADAR_RECORDS_LIST_FIELD_NUMBER: _ClassVar[int]
    radar_records_list: _containers.RepeatedCompositeFieldContainer[RadarHistoryRecord]
    def __init__(self, radar_records_list: _Optional[_Iterable[_Union[RadarHistoryRecord, _Mapping]]] = ...) -> None: ...
