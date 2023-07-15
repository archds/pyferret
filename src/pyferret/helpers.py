from typing import Iterable, TypeVar

from pyferret import maybe

S = TypeVar("S")


def from_optional(value: S | None) -> maybe.Maybe[S]:
    if value is not None:
        return maybe.Just(value)
    else:
        return maybe.Nothing()


def concat(iterable: Iterable[Iterable[S]]) -> list[S]:
    return [item for sublist in iterable for item in sublist]
