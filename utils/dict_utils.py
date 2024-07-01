def invert_dict(dictionary: dict) -> dict:
    temp_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict) or isinstance(value, list):
            pass
        else:
            temp_dict.update({value: key})
    return temp_dict


def safe_pop(dictionary: dict, keys: list):
    """
    Safely remove the specified keys in a dictionary.
    """
    if not isinstance(keys, list):
        keys = [keys]

    for key in keys:
        if key in dictionary:
            dictionary.pop(key)
