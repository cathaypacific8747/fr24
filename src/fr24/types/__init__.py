from datetime import datetime
from typing import TypeVar, Union

from typing_extensions import TypeAlias

M = TypeVar("M")
"""Method"""


IntTimestampS: TypeAlias = int
"""Unix timestamp in integer seconds."""
IntTimestampMs: TypeAlias = int
"""Unix timestamp in integer milliseconds."""
IntoTimestamp: TypeAlias = Union[IntTimestampS, datetime]
"""A type that can be converted to a timestamp (in seconds)."""


IntFlightId: TypeAlias = int
"""Flight ID as an integer."""
StrFlightIdHex: TypeAlias = str
"""Flight ID as a hexadecimal string."""
IntoFlightId: TypeAlias = Union[IntFlightId, StrFlightIdHex, bytes]
"""A type that can be converted to a flight ID."""
