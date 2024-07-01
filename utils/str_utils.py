import re
from ast import literal_eval


def str_to_bool(string: str):
    return string in ["1", "true", True]


def remove_quotes(input_string: str):
    return re.sub(r"^'(.*)'$", r"\1", input_string)
