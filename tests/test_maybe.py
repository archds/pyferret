from maybe import Just, Maybe, Nothing


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


def test_bind() -> None:
    def multiply_by_two(x: int) -> Maybe[int]:
        return Just(x * 2)

    def return_nothing(_: int) -> Maybe[int]:
        return Nothing()

    just_val = Just(1)
    nothing_val = Nothing()

    just_multiplied_by_two = just_val.bind(multiply_by_two)
    just_on_nothing = just_val.bind(return_nothing)

    nothing_multiplied_by_two = nothing_val.bind(multiply_by_two)
    nothing_on_nothing = nothing_val.bind(return_nothing)

    assert just_multiplied_by_two._value == just_val._value * 2
    assert just_on_nothing._value is None
    assert nothing_multiplied_by_two._value is None
    assert nothing_on_nothing._value is None


def test_partial_bind() -> None:
    def multiply(x: int, y: int) -> Maybe[int]:
        return Just(x * y)
    
    just_val = Just(1)
    nothing_val = Nothing()
    
    just_multiplied_by_three = just_val.bind_partial(multiply, 3)
    nothing_multiplied_by_three = nothing_val.bind_partial(multiply, 3)
    
    
    assert just_multiplied_by_three._value == just_val._value * 3
    assert nothing_multiplied_by_three._value is None
    
def test_bind_tuple_through() -> None:
    pass