import re
from urllib.parse import urlparse

from utils.str_utils import remove_quotes


def is_url(string, raiseErrors=True):
    string = remove_quotes(string)
    try:
        parsed_url = urlparse(string)
        if all([parsed_url.scheme, parsed_url.netloc]):
            return string
        else:
            if raiseErrors:
                raise ValueError("not a valid url.")
    except ValueError as e:
        if raiseErrors:
            raise e