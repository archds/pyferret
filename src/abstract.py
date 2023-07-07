from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
S = TypeVar("S")


class Context(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, v: T) -> None:
        self._value = v


class Functor(Context[T]):
    @abstractmethod
    def fmap(self, func: Callable[[T], S]) -> Functor[S]:
        raise NotImplementedError

    @abstractmethod
    def fmap_partial(
        self,
        func: Callable[[T, Any], S],
        *args,
        **kwargs,
    ) -> Functor[S]:
        raise NotImplementedError

    @abstractmethod
    def fmap_tuple(self, func: Callable[[Any], S], take: int) -> Functor[S]:
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
        raise NotImplementedError

    @abstractmethod
    def bind_partial(
        self,
        func: Callable[[T, Any], Monad[S]],
        *args,
        **kwargs,
    ) -> Monad[S]:
        raise NotImplementedError

    @abstractmethod
    def bind_tuple(self, func: Callable[[Any], Monad[S]], take: int) -> Monad[S]:
        raise NotImplementedError
