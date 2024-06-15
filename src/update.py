import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.functions import find_files, get_updated_file_content, get_updated_functions
from utils.path_utils import is_valid_path
from utils.parser import *
from utils.dict_utils import (
    get_item_case_insensitive,
)
from src.constants import *


def detect_language(file_path: str):
    is_valid_path(file_path)
    extension = os.path.splitext(file_path)[1]

    for key, vals in languages_metadata.items():
        extensions = vals.get("extensions")
        if extensions and extension in extensions:
            key: str
            return key.lower()

    return "python"


def get_function_patterns(
    file_path: str, language: str = None, function_patterns: list = None
):
    if function_patterns:
        return function_patterns

    if not language:
        language = detect_language(file_path)

    default_patterns = ["\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def|\\Z)"]
    l = get_item_case_insensitive(languages_metadata, language)

    if not l:
        return default_patterns
    else:
        l: dict
        return l.get("function_patterns", default_patterns)


def update(
    update_files: list = update_files,
    update_source_directory: str = update_source_directory,
    update_destination_directory: str = update_destination_directory,
    language: str = None,
    function_patterns: list = None,
):

    if not update_files:
        update_files = [file for file in os.listdir(update_source_directory)]

    print(
        f'Updating changed files from "{update_source_directory}" to "{update_destination_directory}"...'
    )

    # find specified files in source directory

    source_files = find_files(update_source_directory, update_files)
    update_source_directory = os.path.normpath(update_source_directory)
    update_destination_directory = os.path.normpath(update_destination_directory)

    funcs = []
    updated_content = ""

    for source_path in source_files:

        source_file_name = os.path.basename(source_path)
        dir_name = os.path.dirname(source_path)

        if dir_name != update_source_directory:
            base_dir = os.path.basename(os.path.dirname(source_path))
            update_path = os.path.normpath(
                f"{update_destination_directory}/{base_dir}/{source_file_name}"
            )
        else:
            update_path = os.path.normpath(
                f"{update_destination_directory}/{source_file_name}"
            )

        if not is_valid_path(update_path, False):  # file does not exist, copy it
            # copy file
            print(
                f"File '{source_file_name}' not found in '{update_destination_directory}'. \n Copying to '{update_path}'..."
            )
            subprocess.run(["cp", source_path, update_path])
        else:
            # get updated content and write it to file
            function_patterns = get_function_patterns(
                source_path, language, function_patterns
            )
            funcs = get_updated_functions(source_path, update_path, function_patterns)
            content = get_updated_file_content(funcs, update_path)

            with open(update_path, "w", encoding="utf-8") as file:
                file.write(content)

        pp.pprint([f"Source path: {source_path}", f"Update path: {update_path}"])

    return source_files, funcs, updated_content


if __name__ == "__main__":

    parser_arguments = [
        Argument(name=("-f", "--update_files"), nargs="+"),
        Argument(name=("-l", "--language")),
        DirectoryArgument(name=("-s", "--update_source_directory")),
        DirectoryArgument(name=("-d", "--update_destination_directory")),
        Argument(name=("-p", "--function_patterns"), nargs="+"),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    # print(args)
    update(**args)
