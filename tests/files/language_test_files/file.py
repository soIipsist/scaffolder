def some_decorator(func):
    def wrapper(*args, **kwargs):
        print("some_decorator: Before function call")
        result = func(*args, **kwargs)
        print("some_decorator: After function call")
        return result

    return wrapper


def simple_function():
    print("This is a simple function.")


def function_with_args(arg1, arg2):
    return arg1 + arg2


def function_with_default_args(arg1, arg2=10):
    return arg1 + arg2


def function_with_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(f"{key} = {value}")


def function_with_args_and_kwargs(arg1, *args, **kwargs):
    print(arg1)
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(f"{key} = {value}")


def function_with_annotations(arg1: int, arg2: str) -> str:
    return f"{arg1} {arg2}"


def generator_function():
    yield 1
    yield 2
    yield 3


async def async_function():
    await asyncio.sleep(1)
    return "async result"


class MyClass:
    def method(self):
        print("This is a method.")

    @staticmethod
    def static_method():
        print("This is a static method.")

    @classmethod
    def class_method(cls):
        print("This is a class method.")


# Decorated function
@some_decorator
def decorated_function():
    print("This is a decorated function.")


# Lambda function assigned to a variable
lambda_function = lambda x: x * 2


# Function with type hinting
def function_with_type_hints(arg1: int, arg2: float) -> float:
    return arg1 + arg2


# Function with multiline arguments
def multiline_arguments_function(
    arg1,
    arg2,
    arg3,
):
    return arg1 + arg2 + arg3


if __name__ == "__main__":
    simple_function()
    print(function_with_args(1, 2))
    print(function_with_default_args(1))
    function_with_kwargs(a=1, b=2)
    function_with_args_and_kwargs(1, 2, 3, a=4, b=5)
    print(function_with_annotations(1, "test"))
    for value in generator_function():
        print(value)
    import asyncio

    print(asyncio.run(async_function()))
    obj = MyClass()
    obj.method()
    MyClass.static_method()
    MyClass.class_method()
    decorated_function()
    print(lambda_function(3))
    print(function_with_type_hints(1, 2.0))
    print(multiline_arguments_function(1, 2, 3))
