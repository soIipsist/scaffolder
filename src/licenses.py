import subprocess
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.file_utils import read_file, overwrite_file
from utils.path_utils import is_valid_path
from utils.parser import *
from src.constants import *
import re


def get_license_paths(licenses: list = []):
    license_paths = [
        path
        for license in licenses
        if (path := is_valid_path(os.path.join(licenses_directory, license), False))
        is not None
    ]

    return license_paths


def create_license(license: str, destination_directory: str, author: str, year: str):
    license_path = get_license_paths([license])[0]

    # check if license exists
    project_license_path = os.path.join(destination_directory, "LICENSE")
    update = os.path.exists(project_license_path)

    if update:
        os.remove(project_license_path)

    if license_path:
        command = f"cp {license_path} {destination_directory}"
        subprocess.run(command, shell=True)
        return update_license(destination_directory, license, author, year)


def update_license(destination_directory: str, license: str, author: str, year: str):
    # replace where author and year are in license
    new_path = os.path.join(destination_directory, license)
    content = read_file(new_path)

    new_content = re.sub(r"\{author\}", author, content)
    new_content = re.sub(r"\{year\}", str(year), new_content)
    overwrite_file(new_path, new_content)

    # rename to LICENSE
    dest = os.path.join(destination_directory, "LICENSE")
    os.rename(new_path, dest)
    return dest


def view_license(licenses: list = [], show_content: int = 0):

    show_content = bool(show_content)

    if not isinstance(licenses, list):
        licenses = [licenses]

    if licenses == "all" or not licenses:
        license_paths = os.listdir(licenses_directory)
        license_paths = get_license_paths(license_paths)
    else:
        license_paths = get_license_paths(licenses)

    for path in license_paths:
        if show_content:
            content = read_file(path, "utf-8")
            print(content)
        else:
            print(path)

    return license_paths


def main():
    parser_arguments = [
        Argument(name=("-l", "--licenses"), nargs="+"),
        BoolArgument(name=("-c", "--show_content")),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    view_license(**args)


if __name__ == "__main__":
    main()
