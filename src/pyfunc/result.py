from __future__ import annotations

from typing import Any, Callable, TypeAlias, TypeVar

import abstract
import maybe

T = TypeVar("T")
S = TypeVar("S")
U = TypeVar("U")
E = TypeVar("E")


class Ok(abstract.Monad[T]):
    def fmap(self, func: Callable[[T], S]) -> Ok[S]:
        """
        If `Ok[T]` - applies `(T -> S)` and returns `Ok[S]`
        """
        return Ok(func(self._value))

    def fmap_partial(
        self, func: Callable[[T, Any], S], *args, **kwargs
    ) -> Result[S, E]:
        """
        If `Ok[T]` - applies `partial((T -> S), *args, **kwargs)` and returns `Ok[S]`
        """
        return Ok(func(self._value, *args, **kwargs))

    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Ok[S]:
        """
        If `Ok[T]` - applies `partial((T -> S), *args, **kwargs)` and returns `Ok[S]`
        """
        assert isinstance(self._value, tuple)

        return Ok(func(self._value[take]))

    def fmap_through(self, func: Callable[[T], Result[Any, E]]) -> Ok[T]:
        """
        If `Ok[T]` - applies `(T -> Any)` to `T` and returns `Ok[T]`
        """
        _ = func(self._value)

        return self

    def fmap_partial_through(
        self, func: Callable[[T, Any], Result[Any, E]], *args, **kwargs
    ) -> Ok[T]:
        """
        If `Ok[T]` - applies `partial((T -> Any), *args, **kwargs)` to `T` and returns
        `Ok[T]`
        """
        _ = func(self._value, *args, **kwargs)

        return self

    def fmap_tuple_through(
        self, func: Callable[[Any], Result[Any, E]], take: int
    ) -> Ok[T]:
        """
        If `Ok[tuple]` - applies `(T -> S)` to `tuple[take]`, and returns
        `Ok[tuple]`
        """
        assert isinstance(self._value, tuple)

        _ = func(self._value[take])

        return self

    def bind(self, func: Callable[[T], Result[S, E]]) -> Result[S, E]:
        """
        If `Ok[T]` - applying `(T -> Result[S, E])`, and returns `Result[S, E]`
        """
        return func(self._value)

    def bind_partial(
        self, func: Callable[[T, Any], Result[S, E]], *args, **kwargs
    ) -> Result[S, E]:
        """
        If `Ok[T]` - applies `partial((T -> Result[S, E]), *args, **kwargs)` to `T` and
        returns `Result[S, E]`
        """
        return func(self._value, *args, **kwargs)

    def bind_tuple(
        self, func: Callable[[Any], Result[S, E]], take: int
    ) -> Result[S, E]:
        """
        If `Ok[tuple]` - applies `(Any -> Maybe[S])` to `tuple[take]`, and returns
        `Result[S, E]`
        """
        assert isinstance(self._value, tuple)

        return func(self._value[take])

    def bind_through(self, func: Callable[[T], Result[S, E]]) -> Result[T, E]:
        """
        If `Ok[T]` - apply `(T -> Result[S, E])` and:
            - return `Ok[T]` if func result `Ok[Any]`
            - return `Err[E]` if func result `Err[E]`
        """
        result = func(self._value)

        if isinstance(result, Err):
            return result
        else:
            return self

    def bind_partial_through(
        self, func: Callable[[T, Any], Result[S, E]], *args, **kwargs
    ) -> Result[T, E]:
        """
        If `Ok[T]` - apply `partial((T -> Result[S, E]), *args, **kwargs)` and:
            - return `Ok[T]` if func result `Just[Any]`
            - return `Err[E]` if func result `Err[E]`
        """
        result = func(self._value, *args, **kwargs)

        if isinstance(result, Err):
            return result
        else:
            return self

    def bind_tuple_through(
        self, func: Callable[[Any], Result[S, E]], take: int
    ) -> Result[T, E]:
        assert isinstance(self._value, tuple)

        result = func(self._value[take])

        if isinstance(result, Err):
            return result
        else:
            return self

    def bind_maybe(
        self: Ok[maybe.Maybe[S]], func: Callable[[S], Result[U, E]]
    ) -> Result[maybe.Maybe[U], E]:
        if isinstance(self._value, maybe.Just):
            result = func(self._value._value)

            if isinstance(result, Ok):
                return Ok(maybe.Just(result._value))
            else:
                return result

        else:
            return Ok(maybe.Nothing())

    @property
    def is_err(self):
        return False

    @property
    def is_ok(self):
        return True


class Err(abstract.Monad[T]):
    def bind(self, func: Callable[[Any], Result[S, E]]) -> Err[T]:
        raise NotImplementedError

    def bind_maybe(
        self, func: Callable[[S], Result[U, E]]
    ) -> Result[maybe.Maybe[U], E]:
        raise NotImplementedError


Result: TypeAlias = Ok[T] | Err[E]
