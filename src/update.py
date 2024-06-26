import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.functions import find_files, get_updated_file_content, get_updated_functions
from utils.path_utils import is_valid_path
from utils.parser import *
from src.constants import *
from src.languages import detect_language


def get_function_patterns(
    file_path: str, language: str = None, function_patterns: list = None
):
    if function_patterns:
        return function_patterns

    if not language:
        language = detect_language(file_path)

    default_patterns = ["\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def|\\Z)"]

    lang = Language(language=language).select()

    if len(lang) > 0:
        function_patterns = getattr(lang[0], "function_patterns")
        return function_patterns if function_patterns else default_patterns


def update(
    update_files: list = update_files,
    update_template_directory: str = update_template_directory,
    update_destination_directory: str = update_destination_directory,
    language: str = None,
    function_patterns: list = None,
):

    if not update_files:
        update_files = [file for file in os.listdir(update_template_directory)]

    print(
        f'Updating changed files from "{update_template_directory}" to "{update_destination_directory}"...'
    )

    # find specified files in source directory

    source_files = find_files(update_template_directory, update_files)
    update_template_directory = os.path.normpath(update_template_directory)
    update_destination_directory = os.path.normpath(update_destination_directory)

    funcs = []
    updated_content = ""

    for source_path in source_files:

        source_file_name = os.path.basename(source_path)
        dir_name = os.path.dirname(source_path)

        if dir_name != update_template_directory:
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


def main():

    parser_arguments = [
        Argument(name=("-f", "--update_files"), nargs="+"),
        Argument(name=("-l", "--language")),
        DirectoryArgument(name=("-s", "--update_template_directory")),
        DirectoryArgument(name=("-d", "--update_destination_directory")),
        Argument(name=("-p", "--function_patterns"), nargs="+"),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    update(**args)


if __name__ == "__main__":
    main()
