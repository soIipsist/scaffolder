import os
import subprocess
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.functions import find_files, get_updated_file_content, get_updated_functions
from templates.python_template.utils.path_operations import is_valid_path
from templates.python_template.utils.parser import *
from src.constants import *


def update(
    update_files: list = update_files,
    update_source_directory: str = update_source_directory,
    update_destination_directory: str = update_destination_directory,
    language: str = "python",
    function_patterns: list = None,
):  

    if not update_files:
        update_files = [file for file in os.listdir(update_source_directory)]
    
    print(
        f'Updating changed files from "{update_source_directory}" to "{update_destination_directory}"...'
    )

    if language not in languages:
        raise ValueError(
            "Language not supported. Look at 'function_patterns.json' to check for all supported languages."
        )

    # always use function patterns array, if defined

    if not function_patterns:
        function_patterns = function_patterns_metadata.get(language)

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
            update_path = os.path.normpath(f"{update_destination_directory}/{source_file_name}")

        if not is_valid_path(update_path, False):  # file does not exist, copy it
            # copy and paste file
            print(
                f"File '{source_file_name}' not found in '{update_destination_directory}'. \n Copying to '{update_path}'..."
            )
            subprocess.run(["cp", source_path, update_path])
        else:
            # get updated content and write it to file
            funcs = get_updated_functions(source_path, update_path, function_patterns)
            content = get_updated_file_content(funcs, update_path)

            # print(content)

            with open(update_path, "w", encoding="utf-8") as file:
                file.write(content)

        pp.pprint([f"Source path: {source_path}", f"Update path: {update_path}"])

    return source_files, funcs, updated_content

if __name__ == "__main__":

    parser_arguments = [
        Argument(name=('-f','--update_files'), nargs='+'),
        DirectoryArgument(name=('-s', '--update_source_directory')),
        DirectoryArgument(name=('-d', '--update_destination_directory')),
        Argument(name=('-p', '--function_patterns'), nargs='+')
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    # print(args)
    update(**args)