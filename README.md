# pyferret

![Python 3.11](https://img.shields.io/badge/python-3.11-3572a5.svg)
[![PyPI version](https://badge.fury.io/py/pyferret.svg)](https://badge.fury.io/py/pyferret)
![Coverage](coverage.svg)

This Python library provides functional programming tools like the "maybe" and "result" monads. These monads help handle optional values and error handling in a functional way. The "maybe" monad deals with null or undefined values, while the "result" monad manages computations that may fail and return an error. These tools promote clean, reliable, and concise code by promoting immutability, separation of concerns, and composability.

Not pretending on full correspondence with theoretical part of related instruments, because of not all of them can be implemented in Python context with comfortable usage. There may be implemented not all details that required by some abstractions in FP or provided some additional stuff for usability.

- [pyferret](#pyferret)
  - [Installation](#installation)
  - [Function composition](#function-composition)
  - [Meaning of Context](#meaning-of-context)
  - [Value of Functor](#value-of-functor)
  - [Importance of Monad](#importance-of-monad)
  - [Maybe](#maybe)
    - [How `Maybe` can help with function composition?](#how-maybe-can-help-with-function-composition)
    - [`Maybe` API](#maybe-api)
      - [Initialize instance](#initialize-instance)
      - [`isintance` checks](#isintance-checks)
      - [Unsafe accessing the value](#unsafe-accessing-the-value)
      - [Safe accessing the value](#safe-accessing-the-value)
      - [Boolean checks](#boolean-checks)
      - [Mapping functions](#mapping-functions)
      - [Binding functions](#binding-functions)
  - [Result](#result)
    - [How `Result` can help with function composition?](#how-result-can-help-with-function-composition)
    - [`Result` API](#result-api)
      - [Initialize instance](#initialize-instance-1)
      - [`isintance` checks](#isintance-checks-1)
      - [Unsafe accessing the value](#unsafe-accessing-the-value-1)
      - [Safe accessing the value](#safe-accessing-the-value-1)
      - [Boolean checks](#boolean-checks-1)
      - [Mapping functions](#mapping-functions-1)
      - [Binding functions](#binding-functions-1)
  - [Helpers](#helpers)
    - [Maybe from optional](#maybe-from-optional)
    - [List concatenation](#list-concatenation)
  - [TODO](#todo)

## Installation

```bash
pip install pyferret
```

## Function composition

In Python function composition may be quite nice and useful tool. Function composition is a technique in functional programming where multiple functions are combined together to create a new function. The output of one function becomes the input of the next function, forming a chain of transformations. This allows for the creation of complex and reusable logic by breaking it down into smaller, composable parts.

To use a composition that corresponds this description in Python we need some helpful tools which this library provides.

We have some calculating functions:

```python
def compute_x() -> int | None: ...
def compute_y() -> int | None: ...
def calculate_coef(x: int) -> int: ...
def format_result(x: str) -> str: ...
def dispatch(x: str) -> str | None: ...

def process_x() -> str | None:
    computed_x = compute_x()
    if computed_x:
        coef = calculate_coef(computed_x)
        formatted = format_result(str(coef).upper())

        return dispatch(formatted)
```

That simple function take too much visual burden. Despite we declared our function with word "process" it's not look like a actual process. We have one simple condition - if some of processing steps is `None` then we return `None`, and every that step requires an `if` block to handle.

How that can look like with function composition.

```python
from pyferret.maybe import Maybe

def compute_x() -> Maybe[int]: ...
def compute_y() -> Maybe[int]: ...
def calculate_coef(x: int) -> int: ...
def format_result(x: str) -> str: ...
def dispatch(x: str) -> Maybe[str]: ...

# Result type is `Just[str] | Nothing`
def process_x() -> Maybe[str]:
    return (
        compute_x()
        .fmap(calculate_coef)
        .fmap(str)
        .fmap(format_result)
        .fmap(str.upper)
        .bind(dispatch)
    )

# `process_x` is also can be composed in next calls
# `result` type is `Just[int] | Nothing`
result = process_x().fmap(str.lower).fmap(str.split).fmap(len)
```

## Meaning of Context

In functional programming, a context refers to additional information or state associated with a computation or value.

In here context is simple container that stores a single value, but have meaning for us, like a list or tuple with one element. For example we can have 500 as computation result and 500 as error code, same value and different result.

```python
ERROR_CODE = 500

def compute_or_error_code() -> int:
    try:
        _ = 500 / randint(0, 1)
    except ZeroDivisionError:
        return ERROR_CODE

result = compute_or_error_code()
# In this case we have probability that `result` can be an error and
# a computation result

is_error = result == ERROR_CODE  # This may be not an error
```

## Value of Functor

Functor defined here as Context which have `fmap` method.

Let's say we have a Functor named `A` with value `100` (we say that Functor is a Context, while Context is just a container for a value). Then `fmap` simply takes a function that can do operation on type of `A` and packs result of function to same Context.

```python
result = SomeFunctor(100).fmap(str)  # SomeFunctor("100")
```

## Importance of Monad

Monad defined here as Functor which have `bind` method.

Let's say we have a Monad named `A` with value `100`, and function that takes parameter type of `A` and return same Monad `B` with different or same type of context value. So `bind` taking this function, provide operation on value of `A`, and return `B`.

```python
op = lambda x: SomeMonad("Yes!")
result = SomeMonad(100).bind(op)  # SomeMonad("Yes!")
```

## Maybe

A "maybe" monad handles computations that may or may not produce a value. It represents uncertainty or potential failure. The value can be "Just x" or "Nothing". This allows for chaining computations and concise error handling.

Let's dive into example:

```python
def compute_or_none() -> int | None: ...

# Result is the int or None, but None can have meaning in some context,
# None is the object which represents void, but it's not a void, it's value
result = compute_or_none()

ERROR_CODE = 500

def side_effect() -> None | Literal[ERROR_CODE]: ...

result = side_effect()

# In that context None represents success of operation, and value represent
# an error
if result == ERROR_CODE: ...
```

A `Maybe` monad can help to qualify what exactly function will return in that case.

```python
from pyferret.maybe import Maybe, Just, Nothing

def compute_or_none() -> Maybe[int]: ...

result = compute_or_none()

# We can check is value present in result by accessing some properties
if result.is_some: ...

if result.is_nothing: ...

ERROR_CODE = 500

# Same as previous but in manner on `Maybe` usage
def side_effect() -> Maybe[ERROR_CODE]: ...

result = side_effect()

if result.is_some: ...
```

### How `Maybe` can help with function composition?

`Maybe` can be treated as `Just[Any] | Nothing`, where `Just` and `Nothing` is a `Context` that stores a value, but `Nothing` not providing access to inner value because meaning of this word say that there's can't be a value.

We defined that Maybe is a monad, then it have `fmap`, `bind` and other helpful methods.

### `Maybe` API

#### Initialize instance

```python
>>> some = Just(1)
>>> nothing = Nothing()
```

#### `isintance` checks

```python
>>> isinstance(some, Just)
True
>>> isinstance(nothing, Nothing)
True
```

#### Unsafe accessing the value

```python
>>> some.value
1
>>> nothing.value
ValueError: Attempt to get value on Nothing
```

#### Safe accessing the value

```python
>>> some.get_value_or("default")
1
>>> nothing.get_value_or("default")
'default'
```

#### Boolean checks

```python
>>> some.is_some
True
>>> nothing.is_some
False
```

#### Mapping functions

Basic `fmap`:

```python
>>> some.fmap(lambda x: x * 3 * 10)
Just 30
>>> nothing.fmap(lambda x: x * 3 * 10)
Nothing
```

We may need make side effect with value inside `Just`, but preserve this value and ignore function return:

```python
>>> some.fmap_through(lambda x: print(x))
1  # print(x)
Just 1  # print returns `None`, but some.value is preserved in context
>>> nothing.fmap_through(lambda x: print(x))
Nothing
```

Partial application mapped function:

```python
>>> some.fmap_partial(lambda x, y: x * y, y=25)
Just 25
>>> nothing.fmap_partial(lambda x, y: x * y, y=25)
Nothing
```

Partial application with preserving inner value, `fmap_through` and `fmap_partial` combined:

```python
>>> some.fmap_partial_through(lambda x, y: print(x + y), y=25)
26  # print(x + y)
Just 1
>>> nothing.fmap_partial_through(lambda x, y: print(x + y), y=25)
Nothing
```

#### Binding functions

Basic `bind`:

```python
>>> some.bind(lambda x: Just(x + 10))
Just 11
>>> nothing.bind(lambda x: Just(x + 10))
Nothing
>>> some.bind(lambda x: Nothing())
Nothing
>>> nothing.bind(lambda x: Nothing())
Nothing
```

Binding and preserving inner value:

```python
>>> def side_effect(x: int) -> Maybe[str]:
...     print(x)
...     return Just("Ok")
... 
>>> some.bind_through(side_effect)
1
Just 1
>>> nothing.bind_through(side_effect)
Nothing
```

Partial application binding function:

```python
>>> some.bind_partial(lambda x,y: Just(x + y), y=34)
Just 35
>>> nothing.bind_partial(lambda x,y: Just(x + y), y=34)
Nothing
```

Partial application and preserving inner value:

```python
>>> def side_effect(x: int, y: int) -> Maybe[str]:
...     print(x + y)
...     return Just("Ok")
... 
>>> some.bind_partial_through(side_effect, y=42)
43
Just 1
>>> nothing.bind_partial_through(side_effect, y=42)
Nothing
```

## Result

The Result Monad is a way to encapsulate the outcome of a computation in a type that can represent either a successful result or an error.

A little example:

```python
from pyferret.result import Result, Ok, Err

def compute_or_error() -> Result[int, int]: ...

result = compute_or_error()

# We can check success of operation by accessing some properties
if result.is_ok: ...

if result.is_err: ...

ERROR_CODE = 500

# If side-effect may fail
def side_effect() -> Result[None, ERROR_CODE]: ...

result = side_effect()

if result.is_ok: ...
```

### How `Result` can help with function composition?

`Result` can be treated as `Ok[Any] | Err[Any]`, where both `Ok` and `Err` is a `Context` that stores a value, but with semantic about operation result.

Result also have all Monad functions - `fmap`, `bind`.

### `Result` API

#### Initialize instance

```python
>>> ok = Ok(1)
>>> err = Err("error")
```

#### `isintance` checks

```python
>>> isinstance(ok, Ok)
True
>>> isinstance(err, Err)
True
```

#### Unsafe accessing the value

```python
>>> ok.ok_value
1
>>> ok.err_value
ValueError: Attempt to get err value on Ok: 1
>>> err.err_value
'error'
>>> err.ok_value
ValueError: Attempt to get ok value on Err: error
```

#### Safe accessing the value

```python
>>> ok.get_ok_or("default")
1
>>> ok.get_err_or("default")
'default'
>>> err.get_ok_or("default")
'default'
>>> err.get_err_or("default")
'error'
```

#### Boolean checks

```python
>>> ok.is_ok
True
>>> ok.is_err
False
>>> err.is_ok
False
>>> err.is_err
True
```

#### Mapping functions

Basic `fmap`:

```python
>>> ok.fmap(lambda x: x * 3 * 10)
Ok 30
>>> err.fmap(lambda x: x * 3 * 10)
Err error
```

We may need make side effect with value inside `Ok`, but preserve this value and ignore function return:

```python
>>> ok.fmap_through(lambda x: print(x))
1  # print(x)
Ok 1
>>> err.fmap_through(lambda x: print(x))
Err 'error'
```

Partial application mapped function:

```python
>>> ok.fmap_partial(lambda x, y: x * y, y=25)
Ok 25
>>> err.fmap_partial(lambda x, y: x * y, y=25)
Err 'error'
```

Partial application with preserving inner value, `fmap_through` and `fmap_partial` combined:

```python
>>> ok.fmap_partial_through(lambda x, y: print(x + y), y=25)
26  # print(x + y)
Ok 1
>>> err.fmap_partial_through(lambda x, y: print(x + y), y=25)
Err 'error'
```

#### Binding functions

Basic `bind`:

```python
>>> ok.bind(lambda x: Ok(x + 10))
Ok 11
>>> err.bind(lambda x: Ok(x + 10))
Err 'error'
>>> ok.bind(lambda x: Err("another error"))
Err 'another error'
>>> err.bind(lambda x: Err("another error"))
Err 'error'
```

Binding and preserving inner value only in case of `Ok`:

```python
>>> def side_effect(x: int) -> Result[str, str]:
...      print(x)
...      return Ok("Ok")
...
>>> ok.bind_through(side_effect)
1
Ok 1
>>> err.bind_through(side_effect)
Err 'error'

# In that case Err will be taken from `side_effect_error` function
>>> def side_effect_error(x: int) -> Result[str, str]:
...     print(x)
...     return Err("side effect error")
>>> ok.bind_through(side_effect_error)
1
Err 'side effect error'
>>> err.bind_through(side_effect_error)
Err 'error'
```

Partial application binding function:

```python
>>> ok.bind_partial(lambda x,y: Ok(x + y), y=34)
Ok 35
>>> ok.bind_partial(lambda x,y: Err(x + y), y=34)
Err 35
>>> err.bind_partial(lambda x,y: Ok(x + y), y=34)
Err 'error'
>>> err.bind_partial(lambda x,y: Err(x + y), y=34)
Err 'error'
```

Partial application and preserving inner value only if result is `Ok`:

```python
>>> def side_effect(x: int, y: int) -> Result[str, int]:
...     print(x + y)
...     return Ok("Ok")
...
>>> ok.bind_partial_through(side_effect, y=25)
26
Ok 1
>>> err.bind_partial_through(side_effect, y=25)
Err 'error'
>>> ok.bind_partial_through(side_effect_error, y=25)
26
Err 'side effect error'
>>> err.bind_partial_through(side_effect_error, y=25)
Err 'error'
```

## Helpers

Pyfferet provides a set of convenient helper functions to simplify and assist with common tasks.

### Maybe from optional

```python
>>> from pyferret.helpers import from_optional
>>> a: int | None = 12
>>> from_optional(a)
Just 12
>>> a: int | None = None
>>> from_optional(a)
Nothing
```

### List concatenation

```python
>>> concat([[1,2,3], [4,5,6], [7,8,9]])
[1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## TODO

- [x] `Maybe` methods that returns value out of contexts
- [x] `Result` methods that returns value out of contexts
- [x] Complete docs
- [x] `Result` methods for working with exceptions and traceback
- [ ] `Result` methods for fmap and bind `Err` context
- [ ] Helper functions
  - [x] From optional for `Maybe`
  - [x] Concat list
  - [ ] ...
- [x] `Maybe` test coverage
- [x] `Result` test coverage
- [ ] `abstract` test coverage
- [x] `pypi` publish and versioning
- [x] GitGub Actions
  - [x] typecheck
  - [x] codestyle
- [x] Hash and compare methods
- [x] Better `*args` and `**kwargs` typing
