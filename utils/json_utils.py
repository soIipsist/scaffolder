import json


def read_json_file(json_file, errors=None):
    """Returns json data from a file path."""

    try:
        with open(json_file, "r", errors=errors) as file:
            json_object = json.load(file)
            return json_object
    except Exception as e:
        print(e)


def overwrite_json_file(json_file, data):
    """Overwrites an existing json file with data."""
    with open(json_file, "r+") as file:
        file.seek(0)  # rewind
        json.dump(data, file)
        file.truncate()
