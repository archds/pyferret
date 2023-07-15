from pyferret.helpers import concat, from_optional
from pyferret.maybe import Just, Nothing


def test_concat() -> None:
    assert concat([[1, 2, 3], [4, 5, 6], [1, 2, 3]]) == [1, 2, 3, 4, 5, 6, 1, 2, 3]
    assert concat(((1, 2, 3), (4, 5, 6), (1, 2, 3))) == [1, 2, 3, 4, 5, 6, 1, 2, 3]
    assert concat({(1, 2, 3), (4, 5, 6), (1, 2, 3)}) == [1, 2, 3, 4, 5, 6]


def test_from_optional() -> None:
    assert from_optional(None) == Nothing()
    assert from_optional(1) == Just(1)
    assert from_optional(1)._value == 1
