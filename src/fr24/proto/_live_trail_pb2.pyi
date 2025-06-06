"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""

from builtins import (
    int,
)
from collections.abc import (
    Iterable,
)
from fr24.proto._common_pb2 import (
    RadarHistoryRecord,
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
class LiveTrailRequest(Message):
    DESCRIPTOR: Descriptor

    FLIGHT_ID_FIELD_NUMBER: int
    flight_id: int
    def __init__(
        self,
        *,
        flight_id: int = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["flight_id", b"flight_id"]) -> None: ...

@final
class LiveTrailResponse(Message):
    DESCRIPTOR: Descriptor

    RADAR_RECORDS_LIST_FIELD_NUMBER: int
    @property
    def radar_records_list(self) -> RepeatedCompositeFieldContainer[RadarHistoryRecord]:
        """?"""

    def __init__(
        self,
        *,
        radar_records_list: Iterable[RadarHistoryRecord] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: Literal["radar_records_list", b"radar_records_list"]) -> None: ...
