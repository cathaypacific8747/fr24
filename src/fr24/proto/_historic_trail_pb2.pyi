from fr24.proto import _common_pb2 as __common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HistoricTrailRequest(_message.Message):
    __slots__ = ("flight_id",)
    FLIGHT_ID_FIELD_NUMBER: _ClassVar[int]
    flight_id: int
    def __init__(self, flight_id: _Optional[int] = ...) -> None: ...

class HistoricTrailResponse(_message.Message):
    __slots__ = ("radar_records_list",)
    RADAR_RECORDS_LIST_FIELD_NUMBER: _ClassVar[int]
    radar_records_list: _containers.RepeatedCompositeFieldContainer[__common_pb2.RadarHistoryRecord]
    def __init__(self, radar_records_list: _Optional[_Iterable[_Union[__common_pb2.RadarHistoryRecord, _Mapping]]] = ...) -> None: ...
