def str_to_bool(string: str):
    return string in ["1", "true", True]


def snake_to_camel(input_string):
    return "".join(word.title() for word in input_string.split("_"))


def camel_to_snake(input_string):
    import re

    return re.sub(r"(?<!^)(?=[A-Z])", "_", input_string).lower()
