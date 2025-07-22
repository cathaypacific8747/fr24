from datetime import datetime
from typing import Any, Callable, TypeVar, Union

from typing_extensions import TypeAlias

M = TypeVar("M")
"""Method"""


def static_check_signature(dataclass: Any) -> Callable[[M], M]:
    """Marker to signal the static checker that the decorated method
    should have the same signature and documentation as the `__init__` method
    of the given dataclass.

    Note that no checks are performed at runtime: `scripts/check_signature.py`
    is responsible for checking the signature.
    """

    def decorator(method: M) -> M:
        return method

    return decorator


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
