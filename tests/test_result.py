import pytest
from pytest_mock import MockerFixture

from pyferret import maybe
from pyferret.result import Err, Ok, Result


def test_ok_init() -> None:
    value = 2

    item = Ok(value)

    assert item._value == value


def test_err_init() -> None:
    value = "200"

    item = Err(value)

    assert item._value == value


def test_fmap() -> None:
    ok = Ok(200)
    err = Err("200")

    ok_fmap = ok.fmap(lambda x: x * 2)
    err_fmap = err.fmap(str.isdigit)

    assert ok_fmap._value == ok._value * 2
    assert err_fmap._value == err_fmap._value


def test_fmap_partial() -> None:
    ok = Ok(200)
    err = Err("200")

    ok_fmap = ok.fmap_partial(lambda x, y: x * y, y=32)
    err_fmap = err.fmap_partial(lambda x, y: x * y, y=32)

    assert ok_fmap._value == ok._value * 32
    assert err_fmap._value == err_fmap._value


def test_fmap_through(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=30)

    ok = Ok(200)
    err = Err("200")

    ok_fmap = ok.fmap_through(foo)
    err_fmap = err.fmap_through(foo)

    foo.assert_called_once_with(ok._value)
    assert ok_fmap._value == ok._value
    assert err_fmap._value == err_fmap._value


def test_fmap_partial_through(mocker: MockerFixture) -> None:
    foo = mocker.MagicMock(return_value=30)

    ok = Ok(200)
    err = Err("200")

    args = (1, 2, 3)
    kwargs = {"a": 1, "b": 2, "c": 3}

    ok_fmap = ok.fmap_partial_through(foo, *args, **kwargs)
    err_fmap = err.fmap_partial_through(foo, *args, **kwargs)

    foo.assert_called_once_with(ok._value, *args, **kwargs)
    assert ok_fmap._value == ok._value
    assert err_fmap._value == err_fmap._value


def test_bind() -> None:
    def multiply_by_two(x: int) -> Result[int, str]:
        return Ok(x * 2)

    def return_err(_: int) -> Result[int, str]:
        return Err("Error")

    def cast_to_str(x: int) -> Result[str, str]:
        try:
            return Ok(str(x))
        except Exception:
            return Err("Error")

    ok = Ok(100)
    err = Err("200")

    ok_on_ok = ok.bind(multiply_by_two).bind(cast_to_str)
    ok_on_error = ok.bind(return_err).bind(cast_to_str)

    err_on_ok = err.bind(multiply_by_two).bind(cast_to_str)
    err_on_err = err.bind(return_err).bind(cast_to_str)

    assert ok_on_ok._value == str(ok._value * 2)
    assert ok_on_error._value == "Error"

    assert err_on_ok._value == err._value
    assert err_on_err._value == err._value


def test_bind_partial() -> None:
    ok = Ok(200)
    err = Err("200")

    ok_on_ok = ok.bind_partial(lambda x, y: Ok(x * y), y=32)
    ok_on_err = ok.bind_partial(lambda x, y: Err("Error" + str(x) + str(y)), y=32)

    err_on_ok = err.bind_partial(lambda x, y: Ok(x * y), y=32)
    err_on_err = err.bind_partial(lambda x, y: Err("Error" + str(x) + str(y)), y=32)

    assert ok_on_ok._value == ok._value * 32
    assert ok_on_err._value == "Error" + str(ok._value) + str(32)

    assert err_on_ok._value == err._value
    assert err_on_err._value == err._value


def test_bind_through(mocker: MockerFixture) -> None:
    foo_ok = mocker.MagicMock(return_value=Ok(30))
    foo_err = mocker.MagicMock(return_value=Err("Error"))

    ok = Ok(200)
    err = Err("200")

    ok_on_ok = ok.bind_through(foo_ok)
    ok_on_err = ok.bind_through(foo_err)

    err_on_ok = err.bind_through(foo_ok)
    err_on_err = err.bind_through(foo_err)

    foo_ok.assert_called_once_with(ok._value)
    foo_err.assert_called_once_with(ok._value)

    assert ok_on_ok._value == ok._value
    assert ok_on_err._value == foo_err.return_value._value

    assert err_on_ok._value == err._value
    assert err_on_err._value == err._value


def test_bind_partial_through(mocker: MockerFixture) -> None:
    foo_ok = mocker.MagicMock(return_value=Ok(30))
    foo_err = mocker.MagicMock(return_value=Err("Error"))

    ok = Ok(200)
    err = Err("200")

    args = (1, 2, 3)
    kwargs = {"a": 1, "b": 2, "c": 3}

    ok_on_ok = ok.bind_partial_through(foo_ok, *args, **kwargs)
    ok_on_err = ok.bind_partial_through(foo_err, *args, **kwargs)

    err_on_ok = err.bind_partial_through(foo_ok, *args, **kwargs)
    err_on_err = err.bind_partial_through(foo_err, *args, **kwargs)

    foo_ok.assert_called_once_with(ok._value, *args, **kwargs)
    foo_err.assert_called_once_with(ok._value, *args, **kwargs)

    assert ok_on_ok._value == ok._value
    assert ok_on_err._value == foo_err.return_value._value

    assert err_on_ok._value == err._value
    assert err_on_err._value == err._value


def test_bind_maybe(mocker: MockerFixture) -> None:
    foo_ok = mocker.MagicMock(return_value=Ok(30))
    foo_err = mocker.MagicMock(return_value=Err("Error"))

    ok_just = Ok(maybe.Just(200))
    ok_nothing = Ok(maybe.Nothing())
    err = Err("200")

    just_on_ok = ok_just.bind_maybe(foo_ok)
    just_on_err = ok_just.bind_maybe(foo_err)

    nothing_on_ok = ok_nothing.bind_maybe(foo_ok)
    nothing_on_err = ok_nothing.bind_maybe(foo_err)

    err_on_ok = err.bind_maybe(foo_ok)
    err_on_err = err.bind_maybe(foo_err)

    foo_ok.assert_called_once_with(ok_just._value._value)
    foo_err.assert_called_once_with(ok_just._value._value)

    assert isinstance(just_on_ok._value, maybe.Just)
    assert isinstance(just_on_err, Err)

    assert just_on_ok._value._value == foo_ok.return_value._value
    assert just_on_err._value == foo_err.return_value._value

    assert nothing_on_ok._value._value == ok_nothing._value._value
    assert nothing_on_err._value._value == ok_nothing._value._value

    assert err_on_ok._value == err._value
    assert err_on_err._value == err._value


def test_boolean_checks() -> None:
    ok = Ok(200)
    err = Err("200")

    assert ok.is_ok
    assert not err.is_ok

    assert err.is_err
    assert not err.is_ok


def test_value_getter() -> None:
    ok = Ok(200)
    err = Err("200")

    assert ok.ok_value == ok._value
    assert err.err_value == err._value

    with pytest.raises(expected_exception=ValueError):
        err.ok_value
        ok.err_value