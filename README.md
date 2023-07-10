# pyferret

This Python library provides functional programming tools like the "maybe" and "result" monads. These monads help handle optional values and error handling in a functional way. The "maybe" monad deals with null or undefined values, while the "result" monad manages computations that may fail and return an error. These tools promote clean, reliable, and concise code by promoting immutability, separation of concerns, and composability.

Not pretending on full correspondence with theoretical part of related instruments, because of not all of them can be implemented in Python context with comfortable usage. There may be implemented not all details that required by some abstractions in FP or provided some additional stuff for usability.

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

### Meaning of Context

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

### Value of Functor

Functor defined here as Context which have `fmap` method. 

Let's say we have a Functor named `A` with value `100` (we say that Functor is a Context, while Context is just a container for a value). Then `fmap` simply takes a function that can do operation on type of `A` and packs result of function to same Context.

```python
result = SomeFunctor(100).fmap(str)  # SomeFunctor("100")
```

### Importance of Monad

Monad defined here as Functor which have `bind` method.

Let's say we have a Monad named `A` with value `100`, and function that takes parameter type of `A` and return same Monad `B` with different or same type of context value. So `bind` taking this function, provide operation on value of `A`, and return `B`.

```python
op = lambda x: SomeMonad("Yes!")
result = SomeMonad(100).bind(op)  # SomeMonad("Yes!")
```

### Maybe...

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

#### How `Maybe` can help with function composition?

`Maybe` is can be treated as `Just[Any] | Nothing`, where `Just` and `Nothing` is a `Context` that stores a value, but `Nothing` not providing access to inner value because meaning of this word say that there's can't be a value.

We defined that Maybe is a monad, then it have `fmap`, `bind` and other helpful methods.

# Work in progress...

### TODO

- [ ] `Maybe` methods that returns value out of contexts
- [ ] Complete docs
- [ ] `Result` methods for working with exceptions and traceback
- [ ] Helper functions
- [ ] `Maybe` test coverage
- [ ] `Result` test coverage
- [ ] `abstract` test coverage