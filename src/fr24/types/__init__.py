from typing import Callable, TypeVar, cast

from typing_extensions import Concatenate, ParamSpec

#
# In this library, we have a clear separation between
# core functions (e.g. `fr24.json.flight_list`) and
# higher-level OOP wrappers (e.g. `fr24.flight_list.fetch()`).
#
# Core functions accept a `dataclass` as request params
# (e.g. `FlightListParams`) which has extensive documentation for each member.
# To avoid having to rewrite same documentation for its higher level counterpart
# , the following decorator copies the signature from a target `dataclass`.
#
# IDEs will show the correct signature for the higher-level function and MyPy
# will also be happy with it.
#

T = TypeVar("T")
"""origin return type"""
P = ParamSpec("P")
"""origin parameter type"""
S = TypeVar("S")
"""Extra `self` in target method"""
R = TypeVar("R")
"""Actual return type"""


def overwrite_args_signature_from(
    _origin: Callable[P, T],
) -> Callable[
    [Callable[Concatenate[S, ...], R]], Callable[Concatenate[S, P], R]
]:
    """
    Override the argument signature of some target callable with that of an
    `origin` callable. Keeps the target return type intact.

    # Examples

    ```pycon
    >>> from typing import Any
    >>> from fr24.types import overwrite_args_signature_from
    >>> def foo(a: int, b: int) -> float:
    ...     ...
    >>> @overwrite_args_signature_from(foo)
    ... def bar(args: Any, kwargs: Any) -> str:
    ...     return str(foo(*args, **kwargs))
    >>> # IDEs will now show `bar` as having signature
    >>> # `Callable[[int, int], str]`
    ```
    """
    # NOTE: when mkdocs builds the docs, it will not show the signature of `foo`
    # but rather the signature of `bar`.

    def decorator(
        target: Callable[Concatenate[S, ...], R],
    ) -> Callable[Concatenate[S, P], R]:
        return cast(Callable[Concatenate[S, P], R], target)

    return decorator
