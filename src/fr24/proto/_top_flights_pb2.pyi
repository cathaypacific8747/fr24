from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FollowedFlight(_message.Message):
    __slots__ = ("flight_id", "live_clicks", "total_clicks", "flight_number", "callsign", "squawk", "from_iata", "from_city", "to_iata", "to_city", "type", "full_description")
    FLIGHT_ID_FIELD_NUMBER: _ClassVar[int]
    LIVE_CLICKS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_CLICKS_FIELD_NUMBER: _ClassVar[int]
    FLIGHT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    FROM_IATA_FIELD_NUMBER: _ClassVar[int]
    FROM_CITY_FIELD_NUMBER: _ClassVar[int]
    TO_IATA_FIELD_NUMBER: _ClassVar[int]
    TO_CITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FULL_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    flight_id: int
    live_clicks: int
    total_clicks: int
    flight_number: str
    callsign: str
    squawk: int
    from_iata: str
    from_city: str
    to_iata: str
    to_city: str
    type: str
    full_description: str
    def __init__(self, flight_id: _Optional[int] = ..., live_clicks: _Optional[int] = ..., total_clicks: _Optional[int] = ..., flight_number: _Optional[str] = ..., callsign: _Optional[str] = ..., squawk: _Optional[int] = ..., from_iata: _Optional[str] = ..., from_city: _Optional[str] = ..., to_iata: _Optional[str] = ..., to_city: _Optional[str] = ..., type: _Optional[str] = ..., full_description: _Optional[str] = ...) -> None: ...

class TopFlightsRequest(_message.Message):
    __slots__ = ("limit",)
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    limit: int
    def __init__(self, limit: _Optional[int] = ...) -> None: ...

class TopFlightsResponse(_message.Message):
    __slots__ = ("scoreboard_list",)
    SCOREBOARD_LIST_FIELD_NUMBER: _ClassVar[int]
    scoreboard_list: _containers.RepeatedCompositeFieldContainer[FollowedFlight]
    def __init__(self, scoreboard_list: _Optional[_Iterable[_Union[FollowedFlight, _Mapping]]] = ...) -> None: ...
