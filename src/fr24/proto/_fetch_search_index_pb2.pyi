from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FlightSearchData(_message.Message):
    __slots__ = ("reg", "schd_from", "schd_to", "flight", "operator", "ac_type", "lat", "lon", "callsign", "id", "restricted")
    REG_FIELD_NUMBER: _ClassVar[int]
    SCHD_FROM_FIELD_NUMBER: _ClassVar[int]
    SCHD_TO_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_FIELD_NUMBER: _ClassVar[int]
    OPERATOR_FIELD_NUMBER: _ClassVar[int]
    AC_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RESTRICTED_FIELD_NUMBER: _ClassVar[int]
    reg: str
    schd_from: str
    schd_to: str
    flight: str
    operator: str
    ac_type: str
    lat: float
    lon: float
    callsign: str
    id: int
    restricted: bool
    def __init__(self, reg: _Optional[str] = ..., schd_from: _Optional[str] = ..., schd_to: _Optional[str] = ..., flight: _Optional[str] = ..., operator: _Optional[str] = ..., ac_type: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., callsign: _Optional[str] = ..., id: _Optional[int] = ..., restricted: bool = ...) -> None: ...

class FetchSearchIndexRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class FetchSearchIndexResponse(_message.Message):
    __slots__ = ("flights_list",)
    FLIGHTS_LIST_FIELD_NUMBER: _ClassVar[int]
    flights_list: _containers.RepeatedCompositeFieldContainer[FlightSearchData]
    def __init__(self, flights_list: _Optional[_Iterable[_Union[FlightSearchData, _Mapping]]] = ...) -> None: ...
