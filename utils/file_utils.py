from io import BytesIO
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


def download_file(
    url: str,
    destination: str = None,
    content_length=None,
    chunk_size=256,
    timeout=None,
    allow_redirects=True,
    return_response=True,
) -> requests.Response:
    """Downloads a file from the specified URL and saves it to the provided destination path."""

    dl = 0
    try:
        response = requests.get(
            url, stream=True, timeout=timeout, allow_redirects=allow_redirects
        )
        print("Status code: ", response.status_code)

        if response.status_code == 200 and destination:
            with open(destination, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if content_length:  # content length exists
                        content_length = int(content_length)
                        dl += len(chunk)
                        print(dl, "/", content_length)
                    f.write(chunk)

        return response if return_response else destination

    except Exception as e:
        print(e)


def download_file_with_buffer(
    url: str, destination: str = None, content_length=None, chunk_size=256
) -> requests.Response:
    """Downloads a file from the specified URL and saves it to the provided destination path."""

    content_buffer = BytesIO()
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

                    content_buffer.write(chunk)
                    f.write(chunk)
        else:
            print(f"Failed to download. Status code: {response.status_code}")
            return None

        return content_buffer

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

    except Exception as e:
        print(e)


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
