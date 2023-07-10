from __future__ import annotations

from typing import Any, Callable, NoReturn, TypeAlias, TypeVar

from pyferret import abstract, result

T = TypeVar("T", covariant=True)
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

    def bind_result(
        self, func: Callable[[T], result.Result[S, E]]
    ) -> result.Result[Maybe[S], E]:
        """
        If `Just[T]` - apply (T -> Result[S, E]) and return Result[Maybe[S], E]
        """
        res = func(self._value)

        if isinstance(res, result.Ok):
            return result.Ok(Just(res._value))
        else:
            return res

    @property
    def is_some(self) -> bool:
        """
        Return `True` in case of `Just`
        """
        return True

    @property
    def value(self) -> T:
        """
        Unsafe return inner value in case of `Just`
        """
        return self._value

    def get_value_or(self, default: S) -> T:
        """
        If `Just` return inner value
        """
        return self._value

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

    def bind_result(
        self, func: Callable[[T], result.Result[S, E]]
    ) -> result.Ok[Nothing]:
        """
        If `Nothing` returns `Ok[Nothing]`
        """
        return result.Ok(self)

    @property
    def is_some(self) -> bool:
        """
        Return `False` in case of `Nothing`
        """
        return False

    @property
    def value(self) -> NoReturn:
        """
        If `Nothing` raises an error
        """
        raise ValueError("Attempt to get value on Nothing")

    def get_value_or(self, default: S) -> S:
        """
        If `Just` return inner value
        """
        return default

    def __repr__(self) -> str:
        return "Nothing"


Maybe: TypeAlias = Just[T] | Nothing
