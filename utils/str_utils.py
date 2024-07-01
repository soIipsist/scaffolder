import re
from ast import literal_eval


def str_to_bool(string: str):
    return string in ["1", "true", True]


def remove_quotes(input_string: str):
    return re.sub(r"^'(.*)'$", r"\1", input_string)


def check_str_or_int(arg):
    try:
        return int(arg)
    except ValueError:
        pass
    return arg
