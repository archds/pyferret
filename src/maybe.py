from __future__ import annotations

from typing import Any, Callable, TypeAlias, TypeVar

import abstract
from abstract import Functor, Monad

T = TypeVar("T")
S = TypeVar("S")


class Just(abstract.Monad[T]):
    def bind(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        return func(self._value)

    def bind_partial(
        self,
        func: Callable[[T, Any], Maybe[S]],
        *args,
        **kwargs,
    ) -> Maybe[S]:
        return func(self._value, *args, **kwargs)

    def bind_tuple(self, func: Callable[[Any], Maybe[S]], take: int) -> Maybe[S]:
        assert isinstance(self._value, tuple)

        return func(self._value[take])

    def fmap(self, func: Callable[[T], S]) -> Maybe[S]:
        return Just(func(self._value))

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Maybe[S]:
        return Just(func(self._value, *args, **kwargs))

    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Maybe[S]:
        assert isinstance(self._value, tuple)

        return Just(func(self._value[take]))

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

    def bind_partial(
        self,
        func: Callable[[Any, Any], Maybe[S]],
        *args,
        **kwargs,
    ) -> Maybe[S]:
        return self

    def bind_tuple(self, func: Callable[[Any], Monad[S]], take: int) -> Monad[S]:
        return self

    def fmap(self, func: Callable[[Any], S]) -> Maybe[S]:
        return self

    def fmap_partial(
        self,
        func: Callable[[Any, Any], S],
        *args,
        **kwargs,
    ) -> Functor[S]:
        return self

    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Functor[S]:
        return self

    @property
    def is_some(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Nothing"


Maybe: TypeAlias = Just[T] | Nothing
