from __future__ import annotations

from typing import Any, Callable, NoReturn, TypeAlias, TypeVar

from pyferret import abstract, maybe

T = TypeVar("T", covariant=True)
E = TypeVar("E", covariant=True)
S = TypeVar("S")
U = TypeVar("U")
V = TypeVar("V", bound=object)
K = TypeVar("K", bound=object)
EXC = TypeVar("EXC", bound=Exception)


class Ok(abstract.Monad[T]):
    def fmap(self, func: Callable[[T], S]) -> Ok[S]:
        """
        If `Ok[T]` - applies `(T -> S)` and returns `Ok[S]`
        """
        return Ok(func(self._value))

    def fmap_partial(self, func: Callable[[T, Any], S], *args, **kwargs) -> Ok[S]:
        """
        If `Ok[T]` - applies `partial((T -> S), *args, **kwargs)` and returns `Ok[S]`
        """
        return Ok(func(self._value, *args, **kwargs))

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

    def bind_maybe(
        self: Ok[maybe.Maybe[S]], func: Callable[[S], Result[U, E]]
    ) -> Result[maybe.Maybe[U], E]:
        """
        If `Ok[Maybe[S]]` - apply `(S -> Result[U, E])` and:
            - return `Ok[Maybe[U]]` if func result `Ok[U]`
            - return `Err[E]` if func result `Err[E]`
        """
        if isinstance(self._value, maybe.Just):
            result = func(self._value._value)

            if isinstance(result, Ok):
                return Ok(maybe.Just(result._value))
            else:
                return result

        else:
            return Ok(maybe.Nothing())

    @property
    def is_err(self) -> bool:
        """
        If `Ok` return `False`
        """
        return False

    @property
    def is_ok(self) -> bool:
        """
        If `Ok` return `True`
        """
        return True

    @property
    def ok_value(self) -> T:
        """
        Unsafe return ok inner value
        """
        return self._value

    @property
    def err_value(self) -> NoReturn:
        """
        Raises ValueError
        """
        raise ValueError(f"Attempt to get err value on Ok: {self._value}")

    def __repr__(self) -> str:
        return f"Ok {self._value}"


class Err(abstract.Monad[E]):
    def fmap(self, func: Callable[[V], K]) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def fmap_partial(self, func: Callable[[V, Any], K], *args, **kwargs) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def fmap_through(self, func: Callable[[V], Result[Any, S]]) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def fmap_partial_through(
        self, func: Callable[[V, Any], Result[Any, S]], *args, **kwargs
    ) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def bind(self, func: Callable[[V], Result[S, U]]) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def bind_partial(
        self, func: Callable[[V, Any], Result[S, U]], *args, **kwargs
    ) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def bind_through(self, func: Callable[[V], Result[S, U]]) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def bind_partial_through(
        self, func: Callable[[V, Any], Result[S, U]], *args, **kwargs
    ) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    def bind_maybe(self, func: Callable[[V], Result[S, U]]) -> Err[E]:
        """
        If `Err[E]` returns `Err[E]`
        """
        return self

    @property
    def is_err(self):
        """
        If `Err` return `True`
        """
        return True

    @property
    def is_ok(self):
        """
        If `Err` return `False`
        """
        return False

    @property
    def ok_value(self) -> NoReturn:
        """
        Raises ValueError
        Supports Exceptions and shows a cause if inner value is BaseException subclass
        """
        if isinstance(self._value, BaseException):
            raise ValueError(
                f"Attempt to get ok value on Err: {self._value.__class__.__name__}"
            ) from self._value

        raise ValueError(f"Attempt to get ok value on Err: {self._value}")

    @property
    def err_value(self) -> E:
        """
        Unsafe return err inner value
        """
        return self._value

    def __repr__(self) -> str:
        return f"Err {self._value}"


Result: TypeAlias = Ok[T] | Err[E]
