from __future__ import annotations

from typing import Any, Callable, TypeAlias, TypeVar

import abstract

T = TypeVar("T")
S = TypeVar("S")


class Just(abstract.Monad[T]):
    def bind(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        return func(self._value)

    def fmap(self, func: Callable[[T], S]) -> Maybe[S]:
        return Just(func(self._value))

    def applicate(self, func: Maybe[Callable[[T], S]]) -> Maybe[S]:
        if isinstance(func, Just):
            return Just(func._value(self._value))
        else:
            return Nothing()

    @property
    def is_some(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Just {self._value}"


class Nothing(abstract.Monad):
    def __init__(self) -> None:
        self._value = None

    def bind(self, func: Callable[[Any], Maybe[S]]) -> Maybe[S]:
        return self

    def fmap(self, func: Callable[[Any], S]) -> Maybe[S]:
        return self

    @property
    def is_some(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Nothing"


Maybe: TypeAlias = Just[T] | Nothing
