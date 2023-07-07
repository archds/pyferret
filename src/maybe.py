from __future__ import annotations

from typing import Any, Callable, TypeAlias, TypeVar

import abstract

T = TypeVar("T")
S = TypeVar("S")
TU = TypeVar("TU", bound=tuple)


class Just(abstract.Monad[T]):
    def fmap(self, func: Callable[[T], S]) -> Maybe[S]:
        """
        If `Just[T]` - applies `(T -> S)` to `T` and returns `Just[S]`
        """
        return Just(func(self._value))

    def fmap_through(self, func: Callable[[T], Any]) -> Maybe[T]:
        """
        If `Just[T]` - applies `(T -> Any)` to `T` and returns `Just[T]`
        """
        _ = func(self._value)
        return self

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Maybe[S]:
        """
        If `Just[T]` - applies `partial((T -> S), *args, **kwargs)` to `T` and returns
        `Just[S]`
        """
        return Just(func(self._value, *args, **kwargs))

    def fmap_partial_through(
        self, func: Callable[[T, Any], Any], *args, **kwargs
    ) -> Maybe[T]:
        """
        If `Just[T]` - applies `partial((T -> Any), *args, **kwargs)` to `T` and returns
        `Just[T]`
        """
        _ = func(self._value, *args, **kwargs)

        return self

    def fmap_tuple(self, func: Callable[[T], S], take: int) -> Maybe[S]:
        """
        If `Just[tuple]` - applies `(T -> S)` to `tuple[take]`, and returns `Just[S]`
        """
        assert isinstance(self._value, tuple)

        return Just(func(self._value[take]))

    def fmap_tuple_through(self, func: Callable[[T], Any], take: int) -> Maybe[T]:
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

    @property
    def is_some(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f"Just {self._value}"


class Nothing(abstract.Monad[T]):
    def __init__(self) -> None:
        self._value = None

    def fmap(self, func: Callable[[T], S]) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_tuple(self, func: Callable[[TU], S], take: int) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_through(self, func: Callable[[T], Any]) -> Maybe[T]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_partial_through(
        self, func: Callable[[T, Any], Any], *args, **kwargs
    ) -> Maybe[T]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def fmap_tuple_through(self, func: Callable[[T], Any], take: int) -> Maybe[T]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind(self, func: Callable[[T], Maybe[S]]) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_partial(
        self, func: Callable[[T, Any], Maybe[S]], *args, **kwargs
    ) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_tuple(self, func: Callable[[TU], Maybe[S]], take: int) -> Maybe[S]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_through(self, func: Callable[[T], Maybe[Any]]) -> Maybe[T]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_partial_through(
        self, func: Callable[[T, Any], Maybe[Any]], *args, **kwargs
    ) -> Maybe[T]:
        """
        If `Nothing` returns `Nothing`
        """
        return self

    def bind_tuple_through(
        self, func: Callable[[T], Maybe[Any]], take: int
    ) -> Maybe[T]:
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
