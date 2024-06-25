import subprocess
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.file_utils import read_file, overwrite_file
from utils.path_utils import is_valid_path
from utils.parser import *
from src.constants import *
import re
import os


def get_license_paths(licenses=None, licenses_directory=licenses_directory):
    if licenses is None:
        licenses = []

    if licenses == "all":
        return [
            os.path.join(licenses_directory, license)
            for license in os.listdir(licenses_directory)
        ]

    return [
        path
        for license in licenses
        if (path := is_valid_path(os.path.join(licenses_directory, license), False))
        is not None
    ]


def create_license(
    license: str,
    destination_directory: str,
    author: str,
    year: str = year,
):
    if year is None:
        year = datetime.datetime.now().year

    # copy original to destination directory
    license_path = get_license_paths([license])
    license_path = license_path[0] if len(license_path) > 0 else None

    destination_license_path = os.path.join(destination_directory, "LICENSE")

    if license_path:
        command = f"cp {license_path} {destination_license_path}"
        subprocess.run(command, shell=True)

        content = read_file(destination_license_path)
        new_content = re.sub(r"\{author\}", author, content)
        new_content = re.sub(r"\{year\}", str(year), new_content)
        overwrite_file(destination_license_path, new_content)

    return destination_license_path


def view_licenses(
    licenses: list = "all", show_content: bool = False, show_paths: bool = True
):

    license_paths = get_license_paths(licenses)

    for path in license_paths:
        if show_content:
            content = read_file(path, "utf-8")
            print(content)

        if show_paths:
            print(path)

    return license_paths


def main():
    parser_arguments = [
        Argument(name=("-l", "--licenses"), nargs="+"),
        BoolArgument(name=("-p", "--show_paths"), default=False),
        BoolArgument(name=("-c", "--show_content"), default=True),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    view_licenses(**args)


if __name__ == "__main__":
    main()
