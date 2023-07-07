from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, TypeVar

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
