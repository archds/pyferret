from __future__ import annotations

from abc import abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T", covariant=True)
S = TypeVar("S", covariant=True)


class Context(Generic[T]):
    """
    Base class of container that stores some value
    """

    __slots__ = ("_value",)

    def __init__(self, v: T) -> None:
        self._value = v


class Functor(Context[T]):
    @abstractmethod
    def fmap(self, func):
        """
        Applying `func` on inner value of context
        """

        raise NotImplementedError


class Applicative(Functor[T]):
    pass


class Monad(Applicative[T]):
    @abstractmethod
    def bind(self, func):
        """
        Applying `func` which returns a Monad on inner value of context and return its
        result
        """
        raise NotImplementedError
