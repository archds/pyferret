from __future__ import annotations

from typing import Any, Callable, TypeAlias, TypeVar

import abstract
from result import Ok, Result

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")
E = TypeVar("E")


class Just(abstract.Monad[T]):
    def fmap(self, func: Callable[[T], S]) -> Just[S]:
        """
        If `Just[T]` - applies `(T -> S)` to `T` and returns `Just[S]`
        """
        return Just(func(self._value))

    def fmap_through(self, func: Callable[[T], Any]) -> Just[T]:
        """
        If `Just[T]` - applies `(T -> Any)` to `T` and returns `Just[T]`
        """
        _ = func(self._value)
        return self

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Just[S]:
        """
        If `Just[T]` - applies `partial((T -> S), *args, **kwargs)` to `T` and returns
        `Just[S]`
        """
        return Just(func(self._value, *args, **kwargs))

    def fmap_partial_through(
        self, func: Callable[[T, Any], Any], *args, **kwargs
    ) -> Just[T]:
        """
        If `Just[T]` - applies `partial((T -> Any), *args, **kwargs)` to `T` and returns
        `Just[T]`
        """
        _ = func(self._value, *args, **kwargs)

        return self

    def fmap_tuple(self, func: Callable[[T], S], take: int) -> Just[S]:
        """
        If `Just[tuple]` - applies `(T -> S)` to `tuple[take]`, and returns `Just[S]`
        """
        assert isinstance(self._value, tuple)

        return Just(func(self._value[take]))

    def fmap_tuple_through(self, func: Callable[[T], Any], take: int) -> Just[T]:
        """
        If `Just[tuple]` - applies `(T -> S)` to `tuple[take]`, and returns
        `Just[tuple]`
        """
        assert isinstance(self._value, tuple)

        _ = func(self._value[take])

        return self

    def bind(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        """
        If `Just[T]` - applying `(T -> Maybe[S])`, and returns `Maybe[S]`
        """
        return func(self._value)

    def bind_through(self, func: Callable[[T], Maybe[S]]) -> Maybe[T]:
        """
        If `Just[T]` - apply `(T -> Maybe[S])` and:
            - return `Just[T]` if func result `Just[Any]`
            - return `Nothing` if func result `Nothing`
        """
        result = func(self._value)

        if result.is_some:
            return self
        else:
            return Nothing()

    def bind_partial(
        self,
        func: Callable[[T, Any], Maybe[S]],
        *args,
        **kwargs,
    ) -> Maybe[S]:
        """
        If `Just[T]` - applies `partial((T -> Maybe[S]), *args, **kwargs)` to `T` and
        returns `Maybe[S]`
        """
        return func(self._value, *args, **kwargs)

    def bind_partial_through(
        self,
        func: Callable[[T, Any], Maybe[Any]],
        *args,
        **kwargs,
    ) -> Maybe[T]:
        """
        If `Just[T]` - apply `partial((T -> Maybe[S]), *args, **kwargs)` and:
            - return `Just[T]` if func result `Just[Any]`
            - return `Nothing` if func result `Nothing`
        """
        result = func(self._value, *args, **kwargs)

        if result.is_some:
            return self
        else:
            return Nothing()

    def bind_tuple(self, func: Callable[[Any], Maybe[S]], take: int) -> Maybe[S]:
        """
        If `Just[tuple]` - applies `(Any -> Maybe[S])` to `tuple[take]`, and returns
        `Maybe[S]`
        """
        assert isinstance(self._value, tuple)

        return func(self._value[take])

    def bind_tuple_through(
        self, func: Callable[[Any], Maybe[Any]], take: int
    ) -> Maybe[T]:
        """
        If `Just[tuple]` - applies `(Any -> Maybe[Any])` to `tuple[take]`, and returns
        `Maybe[T]`
        """
        assert isinstance(self._value, tuple)

        result = func(self._value[take])

        if result.is_some:
            return self
        else:
            return Nothing()

    def bind_result(
        self: Just[Result[U, E]], func: Callable[[U], Result[S, E]]
    ) -> Just[Result[S, E]]:
        result = self._value

        if isinstance(result, Ok):
            return Just(func(result._value))
        else:
            return Just(result)

    @property
    def is_some(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Just {self._value}"


class Nothing(abstract.Monad[None]):
    def __init__(self) -> None:
        self._value = None

    def fmap(self, func: Callable[[T], S]) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_through(self, func: Callable[[T], Any]) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_partial_through(
        self, func: Callable[[T, Any], Any], *args, **kwargs
    ) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_tuple_through(self, func: Callable[[T], Any], take: int) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind(self, func: Callable[[T], Maybe[S]]) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_partial(
        self, func: Callable[[T, Any], Maybe[S]], *args, **kwargs
    ) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_tuple(self, func: Callable[[Any], Maybe[S]], take: int) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_through(self, func: Callable[[T], Maybe[Any]]) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_partial_through(
        self, func: Callable[[T, Any], Maybe[Any]], *args, **kwargs
    ) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_tuple_through(self, func: Callable[[T], Maybe[Any]], take: int) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_result(self, func: Callable[[U], Result[S, E]]) -> Nothing:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    @property
    def is_some(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Nothing"


Maybe: TypeAlias = Just[T] | Nothing
