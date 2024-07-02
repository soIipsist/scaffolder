import mimetypes
import os
import json
import requests
from toml import loads as load_toml
from toml import dump as dump_toml
from yaml import unsafe_load as load_yaml
from yaml import dump as dump_yaml
from urllib.parse import urlparse
from pandas import read_csv
from xmltodict import parse as parse_xml

from utils.url_utils import is_url

from importlib import resources
import fileinput


def overwrite_file(file_path, content: str, encoding=None, errors=None):
    with open(file_path, "w", encoding=encoding, errors=errors) as file:
        file.write(content)

    return content


def check_file_extension(choices, file_name) -> str:
    """Checks if the provided file path ends in any of the provided extensions."""

    ext = get_file_extension(file_name)
    if ext not in choices or ext == "":
        raise Exception(
            "Invalid file extension. File doesn't end with one of {}".format(choices)
        )
    return file_name


def dump_data_in_file(file_path: str, data=[], errors=None):
    """Dumps data in a file."""

    extension = get_file_extension(file_path)

    dump_data_functions = {"toml": dump_toml, "yaml": dump_yaml, "json": json.dump}
    if extension == "toml" and isinstance(data, list):
        data = {"objects": data}

    try:
        with open(file_path, "w", errors=errors) as file:
            dump_data_functions[extension](data, file)
    except Exception as e:
        print(e)


def load_data(content: str, extension: str = None):
    """Returns parsed content given a specific extension."""

    load_content_functions = {
        "toml": load_toml,
        "yaml": load_yaml,
        "json": json.loads,
        "xml": parse_xml,
    }

    if extension in load_content_functions:
        content = load_content_functions[extension](content)

    return content


def read_and_parse_file(file_path: str, encoding=None, errors=None, base_dir=""):
    """
    Returns the contents of a file. If a file contains data of a specific type, it parses it accordingly.
    """
    if os.path.exists(file_path):
        extension = get_file_extension(file_path)

        if extension == "csv":
            content = read_csv(content)
        else:
            content = read_file(file_path, encoding, errors, base_dir)

    elif is_url(file_path, False):
        response = requests.get(file_path)
        content = response.text
        extension = guess_file_extension(response)
    else:
        raise ValueError("Invalid file or url.")

    return load_data(content, extension)


def read_file(file_path: str, encoding="utf-8", errors=None, package_name=""):
    """
    Returns a file object.
    """

    try:
        with open(file_path, "r", encoding=encoding, errors=errors) as file:
            return file.read()

    except FileNotFoundError:
        # file was not found, return resource if found
        return read_resource_file(file_path, encoding, errors, package_name)

    except (ValueError, json.JSONDecodeError, Exception) as e:
        return f"An error occurred: {e}, {e.__class__}"


def get_file_extension(file):
    """Returns the file extension of a given a file path."""

    return os.path.splitext(file)[1][1:]


def check_file_extension(choices, file_name, raise_exception=True) -> str:
    """Checks if the provided file path ends in any of the provided extensions."""

    ext = get_file_extension(file_name)
    if ext not in choices or ext == "":
        if raise_exception:
            raise Exception(
                "Invalid file extension. File doesn't end with one of {}".format(
                    choices
                )
            )
        return None
    return file_name


def guess_file_extension(response: requests.Response):

    if isinstance(response, requests.Response):
        url = response.url
    elif is_url(response):
        url = response

    url_path = urlparse(url).path
    extension = os.path.splitext(url_path)[1][1:]
    extension = extension if not extension == b"" else None

    if not extension:
        return guess_file_extension_from_headers(response)
    return extension


def guess_file_extension_from_headers(response: requests.Response):
    if not isinstance(response, requests.Response):
        if is_url(response):
            response = requests.get(response)

    content_type = response.headers.get("Content-Type").split(";")[0]
    ext = mimetypes.guess_extension(content_type, strict=False)

    if ext.startswith("."):
        ext = ext.removeprefix(".")

    return ext


def read_resource_file(
    file_path: str, encoding: str = "utf-8", errors=None, package_name: str = ""
):
    from utils.path_utils import path_to_package

    try:
        package_name, resource_name = path_to_package(file_path, package_name)

        print("RESOURCE", package_name, resource_name)
        with (
            resources.files(package_name)
            .joinpath(resource_name)
            .open("r", encoding=encoding, errors=errors) as resource_file
        ):
            return resource_file.read()
    except FileNotFoundError:
        raise ValueError("File not found")
    except (ValueError, json.JSONDecodeError, Exception) as e:
        return f"An error occurred: {e}, {e.__class__}"


def find_and_replace_in_directory(
    directory, search_word, replace_word, removed_dirs: list = []
):
    for root, dirs, files in os.walk(directory):

        for d in removed_dirs:
            if d in dirs:
                dirs.remove(d)

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


def download_file(
    url: str,
    destination: str = None,
    content_length: int = None,
    chunk_size: int = 256,
    timeout: int = None,
    allow_redirects: bool = True,
    return_response: bool = True,
    log_bytes=False,
    log_percentage=True,
) -> requests.Response:
    """Downloads a file from the specified URL and saves it to the provided destination path."""

    dl = 0
    try:
        response = requests.get(
            url, stream=True, timeout=timeout, allow_redirects=allow_redirects
        )
        print("Status code: ", response.status_code)

        if response.status_code == 200 and destination:
            content_length = content_length or int(
                response.headers.get("content-length", 0)
            )

            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    dl += len(chunk)
                    f.write(chunk)
                    if content_length:
                        if log_bytes:
                            print(f"{dl}/{content_length} bytes")

                        if log_percentage:
                            percentage = (dl / content_length) * 100
                            print(f"Downloaded {percentage:.2f}%")

        return response if return_response else destination

    except Exception as e:
        print(e)


def find_files(directory: str, file_names: list):
    """
    Given an array of file names, return a list of valid file paths.
    """

    files = []

    for root, dirs, directory_files in os.walk(directory):
        for file in directory_files:
            file_path = os.path.join(root, file)
            normalized_path = os.path.normpath(file_path)
            base_name = os.path.basename(file_path)

            # Check if the file path or base name matches any in the array
            if file_path in file_names or base_name in file_names:
                files.append(normalized_path)

    return set(files)
