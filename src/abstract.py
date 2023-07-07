from __future__ import annotations

from abc import abstractmethod
from typing import Callable, Generic, TypeVar

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


class Applicative(Functor[T]):
    @abstractmethod
    def applicate(self, func: Applicative[Callable[[T], S]]) -> Applicative[S]:
        raise NotImplementedError


class Monad(Applicative[T]):
    @abstractmethod
    def bind(self, func: Callable[[T], Monad[S]]) -> Monad[S]:
        """
        Applying `func` which returns a Monad on inner value of context and return its
        result
        """
        raise NotImplementedError
