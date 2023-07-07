from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class Context(Generic[T]):
    """
    Base class of container that stores some value
    """

    __slots__ = ("_value",)

    def __init__(self, v: T) -> None:
        self._value = v


class Functor(Context[T]):
    @abstractmethod
    def fmap(self, func: Callable[[T], S]) -> Functor[S]:
        """
        Applying `func` on inner value of context
        """

        raise NotImplementedError

    @abstractmethod
    def fmap_through(self, func: Callable[[T], Any]) -> Functor[T]:
        """
        Same as `fmap`, but returns same context
        """

        raise NotImplementedError

    @abstractmethod
    def fmap_partial(
        self,
        func: Callable[[T, Any], S],
        *args,
        **kwargs,
    ) -> Functor[S]:
        """
        Apply fmap on partial applied `args` and `kwargs` on function `func` that takes
        `T` as first argument

        Same as Functor.fmap(partial(A, *args, **kwargs))
        """

        raise NotImplementedError

    @abstractmethod
    def fmap_partial_through(
        self,
        func: Callable[[T, Any], Any],
        *args,
        **kwargs,
    ) -> Functor[T]:
        """
        Same as `fmap_partial`, but returns same context
        """

        raise NotImplementedError

    @abstractmethod
    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Functor[S]:
        """
        Unsafe and poorly-typed operation which applies `func` to indexed element of
        tuple

        Context value must be a tuple
        """

        raise NotImplementedError

    @abstractmethod
    def fmap_tuple_through(self, func: Callable[[Any], Any], take: int) -> Functor[T]:
        """
        Same as `fmap_tuple`, but returns same context
        """

        raise NotImplementedError


class Applicative(Functor[T]):
    @abstractmethod
    def applicate(self, func: Functor[Callable[[T], S]]) -> Applicative[S]:
        raise NotImplementedError

    @abstractmethod
    def pure(self, value: T) -> Applicative[T]:
        raise NotImplementedError


class Monad(Applicative[T]):
    @abstractmethod
    def bind(self, func: Callable[[T], Monad[S]]) -> Monad[S]:
        """
        Applying `func` which returns a Monad on inner value of context and return its
        result
        """
        raise NotImplementedError

    @abstractmethod
    def bind_through(self, func: Callable[[T], Monad[Any]]) -> Monad[T]:
        """
        Same as `bind` but returns same context
        """
        raise NotImplementedError

    @abstractmethod
    def bind_partial(
        self,
        func: Callable[[T, Any], Monad[S]],
        *args,
        **kwargs,
    ) -> Monad[S]:
        """
        Apply bind on partial applied `args` and `kwargs` on function `func` that takes
        `T` as first argument

        Same as Monad.bind(partial(A, *args, **kwargs))
        """
        raise NotImplementedError

    @abstractmethod
    def bind_partial_through(
        self,
        func: Callable[[T, Any], Monad[Any]],
        *args,
        **kwargs,
    ) -> Monad[T]:
        """
        Same as `bind_partial` but returns same context
        """
        raise NotImplementedError

    @abstractmethod
    def bind_tuple(self, func: Callable[[Any], Monad[S]], take: int) -> Monad[S]:
        """
        Unsafe and poorly-typed operation which applies `func` to indexed element of
        tuple

        Context value must be a tuple
        """

        raise NotImplementedError

    @abstractmethod
    def bind_tuple_through(
        self, func: Callable[[Any], Monad[Any]], take: int
    ) -> Monad[T]:
        """
        Same as `bind_tuple` but returns same context
        """
        raise NotImplementedError
