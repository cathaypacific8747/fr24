from typing import Callable, TypeVar, cast

from typing_extensions import Concatenate, ParamSpec

T = TypeVar("T")
"""origin return type"""
P = ParamSpec("P")
"""origin parameter type"""
S = TypeVar("S")
"""Extra `self` in target"""
R = TypeVar("R")
"""Actual return type"""


# NOTE: this only keeps mypy happy, mkdocs will not show it properly.
# quick hack to reduce code duplication
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
    ... def foo_stringed(args: Any, kwargs: Any) -> str:
    ...     return str(foo(*args, **kwargs))
    >>> # IDEs will now show `foo_stringed` as having signature
    >>> # `Callable[[int, int], str]`
    ```
    """

    def decorator(
        target: Callable[Concatenate[S, ...], R],
    ) -> Callable[Concatenate[S, P], R]:
        return cast(Callable[Concatenate[S, P], R], target)

    return decorator
