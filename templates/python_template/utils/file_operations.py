import os
import json
import requests
import fileinput


def overwrite_file(file_path, content, encoding=None, errors=None):
    with open(file_path, "w", encoding=encoding, errors=errors) as file:
        file.write(content)

    return content


def read_file(file_path, encoding=None, errors=None):
    """
    Returns a file object.
    """
    try:
        with open(file_path, "r", encoding=encoding, errors=errors) as file:
            return file.read()
    except Exception as e:
        return f"An error occurred: {e}"


def read_json_file(json_file, errors=None):
    """Returns json data from a file path."""

    try:
        with open(json_file, "r", errors=errors) as file:
            json_object = json.load(file)
            return json_object
    except Exception as e:
        print(e)


def create_json_file(json_file, data=[]):
    """Creates a new json file if it doesn't exist."""

    try:
        print("Creating JSON file...")
        with open(json_file, "w") as file:
            json.dump(data, file)
    except Exception as e:
        print(e)


def overwrite_json_file(json_file, data):
    """Overwrites an existing json file with data."""
    with open(json_file, "r+") as file:
        file.seek(0)  # rewind
        json.dump(data, file)
        file.truncate()


def append_json_file(json_file, data):
    """Appends data to a json file."""

    existing = read_json_file(json_file)

    if existing is not None:
        with open(json_file, "w+") as outfile:
            existing.append(data)
            outfile.write(json.dumps(existing))
            outfile.close()
    else:
        # create json file and dump empty object
        create_json_file(json_file)
        append_json_file(json_file, data)


def get_file_extension(file):
    """Returns the file extension of a given a file path."""

    return os.path.splitext(file)[1][1:]


def check_file_extension(choices, file_name) -> str:
    """Checks if the provided file path ends in any of the provided extensions."""

    ext = get_file_extension(file_name)
    if ext not in choices or ext == "":
        raise Exception(
            "Invalid file extension. File doesn't end with one of {}".format(choices)
        )
    return file_name


def download_file(
    url: str, destination: str = None, content_length=None, chunk_size=256
) -> requests.Response:
    """Downloads a file from the specified URL and saves it to the provided destination path."""

    dl = 0
    try:
        response = requests.get(url, stream=True)

        if response.status_code == 200 and destination:
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if content_length:  # content length exists
                        content_length = int(content_length)
                        dl += len(chunk)
                        print(dl, "/", content_length)
                    f.write(chunk)
        return response

    except Exception as e:
        print(e)


def find_and_replace_in_directory(directory, search_word, replace_word):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)

            # Rename files containing the keyword
            if search_word in file:
                new_file_name = file.replace(search_word, replace_word)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(file_path, new_file_path)
                file_path = new_file_path

            with fileinput.FileInput(file_path, inplace=True) as f:
                try:
                    for line in f:
                        modified_line = line.replace(search_word, replace_word)
                        print(modified_line, end="")
                except Exception as e:
                    print(e)
