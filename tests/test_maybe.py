import pytest

from pyferret import result
from pyferret.maybe import Just, Maybe, Nothing
from pytest_mock import MockerFixture


def test_just_init() -> None:
    value = 1

    item = Just(value)

    assert item._value == value
    assert item.is_some


def test_nothing_init() -> None:
    item = Nothing()
    assert not getattr(item, "_value", False)
    assert not item.is_some


def test_fmap() -> None:
    def multiply_by_two(x: int) -> int:
        return x * 2

    just_val = Just(1)
    nothing_val = Nothing()

    just_result = just_val.fmap(multiply_by_two)
    nothing_result = nothing_val.fmap(multiply_by_two)

    assert just_result._value == just_val._value * 2
    assert nothing_result._value is None


def test_fmap_through(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=30)

    just_val = Just(1)
    nothing_val = Nothing()

    just_result = just_val.fmap_through(foo)
    nothing_result = nothing_val.fmap_through(foo)

    foo.assert_called_once_with(just_val._value)

    assert just_result._value == 1
    assert nothing_result._value is None


def test_fmap_partial(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=30)

    just_val = Just(1)
    nothing_val = Nothing()

    args = (1, 2, 3)
    kwargs = {"a": 1, "b": 2, "c": 3}

    just_result = just_val.fmap_partial(foo, *args, **kwargs)
    nothing_result = nothing_val.fmap_partial(foo, *args, **kwargs)

    foo.assert_called_once_with(just_val._value, *args, **kwargs)

    assert just_result._value == foo.return_value
    assert nothing_result._value is None


def test_fmap_partial_through(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=30)

    just_val = Just(1)
    nothing_val = Nothing()

    args = (1, 2, 3)
    kwargs = {"a": 1, "b": 2, "c": 3}

    just_result = just_val.fmap_partial_through(foo, *args, **kwargs)
    nothing_result = nothing_val.fmap_partial_through(foo, *args, **kwargs)

    foo.assert_called_once_with(just_val._value, *args, **kwargs)

    assert just_result._value == just_val._value
    assert nothing_result._value is None

def test_bind() -> None:
    def multiply_by_two(x: int) -> Maybe[int]:
        return Just(x * 2)

    def possibly_return_nothing(_: int) -> Maybe[int]:
        return Nothing()

    def cast_to_str(x: int) -> Maybe[str]:
        try:
            return Just(str(x))
        except Exception:
            return Nothing()

    just_val = Just(1)
    nothing_val = Nothing()

    just_multiplied_by_two = just_val.bind(multiply_by_two).bind(cast_to_str)
    just_on_nothing = just_val.bind(possibly_return_nothing).bind(cast_to_str)

    nothing_multiplied_by_two = nothing_val.bind(multiply_by_two)
    nothing_on_nothing = nothing_val.bind(possibly_return_nothing)

    assert just_multiplied_by_two._value == str(just_val._value * 2)
    assert just_on_nothing._value is None
    assert nothing_multiplied_by_two._value is None
    assert nothing_on_nothing._value is None


def test_bind_partial() -> None:
    def multiply(x: int, y: int) -> Maybe[int]:
        return Just(x * y)

    just_val = Just(1)
    nothing_val = Nothing()

    just_multiplied_by_three = just_val.bind_partial(multiply, 3)
    nothing_multiplied_by_three = nothing_val.bind_partial(multiply, 3)

    assert just_multiplied_by_three._value == just_val._value * 3
    assert nothing_multiplied_by_three._value is None


def test_bind_partial_through(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=Just(30))

    just_val = Just(1)
    nothing_val = Nothing()

    args = (1, 2, 3)
    kwargs = {"a": 1, "b": 2, "c": 3}

    just_result = just_val.fmap_partial(foo, *args, **kwargs)
    nothing_result = nothing_val.fmap_partial(foo, *args, **kwargs)

    foo.assert_called_once_with(just_val._value, *args, **kwargs)

    assert just_result._value == foo.return_value
    assert nothing_result._value is None


def test_bind_result() -> None:
    def return_ok(x: int) -> result.Result[int, str]:
        return result.Ok(x * 2)

    def return_err(x: int) -> result.Result[int, str]:
        return result.Err("Error")

    just_val = Just(1)
    nothing_val = Nothing()

    just_on_ok = just_val.bind_result(return_ok)
    just_on_err = just_val.bind_result(return_err)

    nothing_on_ok = nothing_val.bind_result(return_ok)
    nothing_on_err = nothing_val.bind_result(return_err)

    assert isinstance(just_on_ok._value, Just)
    assert isinstance(just_on_err._value, str)

    assert just_on_ok._value._value == just_val._value * 2
    assert just_on_err._value == "Error"

    assert nothing_on_ok._value._value is None
    assert nothing_on_err._value._value is None


def test_is_some() -> None:
    just_val = Just(1)
    nothing_val = Nothing()

    assert just_val.is_some
    assert not nothing_val.is_some


def test_value_getter() -> None:
    just_val = Just(1)
    nothing_val = Nothing()

    assert just_val.value == 1

    with pytest.raises(expected_exception=ValueError):
        nothing_val.value


def test_value_or_default() -> None:
    default = 100

    just_val = Just(1)
    nothing_val = Nothing()

    assert just_val.get_value_or(default) == just_val._value
    assert nothing_val.get_value_or(default) == default
