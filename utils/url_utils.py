import re
from urllib.parse import urlparse


def is_url(string, raise_errors=True):
    from utils.str_utils import remove_quotes

    string = remove_quotes(string)
    try:
        parsed_url = urlparse(string)
        if all([parsed_url.scheme, parsed_url.netloc]):
            return string
        else:
            if raise_errors:
                raise ValueError("not a valid url.")
    except ValueError as e:
        if raise_errors:
            raise e
