import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.functions import (
    get_function_patterns,
    get_updated_file_content,
    get_updated_functions,
    get_function_names,
)
from src.repository import (
    clone_git_repository,
    create_git_repository,
    is_git_repo,
    update_git_repository,
    get_git_origin,
)
from src.licenses import create_license
from src.templates import Template
from utils.file_utils import find_and_replace_in_directory, find_files, overwrite_file
from utils.str_utils import check_str_or_int
from utils.parser import *
from src.constants import *
import shutil


def update_destination_files(
    template_directory: str,
    destination_directory: str,
    language: str = None,
    files: list = [],
    function_patterns: list = [],
    function_names: list = [],
):

    if not files:
        return

    funcs = []
    updated_content = ""

    # if files param is specified, make sure to copy or update those files

    for file in files:

        rel_path = os.path.relpath(file, template_directory)

        # check if directory of rel_path exists in dest
        dest_file = os.path.join(destination_directory, rel_path)

        if not os.path.exists(dest_file):
            print(f"Copying from '{file}' to '{dest_file}'")
            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copyfile(file, dest_file)
        else:
            # file exists in template and in dest
            function_patterns = get_function_patterns(file, language, function_patterns)

            if function_patterns:
                funcs = get_updated_functions(file, dest_file, function_patterns)
                funcs = get_function_names(funcs, function_names)
                content = get_updated_file_content(funcs, dest_file)
                overwrite_file(dest_file, content)

        pp.pprint([f"Source path: {file}", f"Update path: {dest_file}"])

    return files, funcs, updated_content


def check_if_template_exists(template_directory: str = template_directory):
    templ = Template.get_template(template_directory)
    templ: Template

    if templ is None:
        response = input(
            f"Template '{template_directory}' does not exist.\nWould you like to add it as a template? (y/n)"
        )
        if response in ["yes", "y"]:
            templ = Template(template_directory=template_directory)
            templ = templ.add_template(template_directory, True, False)

    return templ


def scaffold_repository(
    git_origin: str,
    create_repository: bool = create_repository,
    repository_visibility: int = repository_visibility,
    destination_directory: str = destination_directory,
):
    if not create_repository:
        return

    if not is_git_repo(destination_directory):
        create_git_repository(git_origin, repository_visibility, destination_directory)
    else:
        update_git_repository(git_origin, repository_visibility, destination_directory)

    return git_origin


def scaffold(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    repository_name: str = repository_name,
    license: str = license,
    author: str = author,
    year: str = year,
    create_repository: bool = create_repository,
    clone_repository: bool = clone_repository,
    store_template: bool = store_template,
    repository_visibility: str = repository_visibility,
    files: list = files,
    language: str = language,
    function_patterns: list = function_patterns,
    function_names: list = function_names,
    replace_name: bool = replace_name,
):

    files = find_files(template_directory, files, ["venv"])

    # copy template if files are not defined
    copy_template = len(files) == 0 or not os.path.exists(destination_directory)

    original_template = check_if_template_exists(template_directory)

    if not original_template:
        return

    repository_name = (
        repository_name if repository_name else os.path.basename(destination_directory)
    )

    new_template = Template(
        template_directory=template_directory,
        template_name=repository_name,
    ).add_template(destination_directory, store_template, copy_template)

    new_template: Template

    if new_template:
        update_destination_files(
            template_directory,
            destination_directory,
            language,
            files,
            function_patterns,
            function_names,
        )

        create_license(license, destination_directory, author, year)

        if replace_name:
            print(
                f"Replacing all instances of '{original_template.template_name}' with '{new_template.template_name}'."
            )
            find_and_replace_in_directory(
                destination_directory,
                original_template.template_name,
                new_template.template_name,
                removed_dirs=[".git"],
            )

        git_origin = get_git_origin(author, repository_name)

        scaffold_repository(
            git_origin, create_repository, repository_visibility, destination_directory
        )

        # clone repository
        if clone_repository:
            shutil.rmtree(destination_directory, ignore_errors=True)
            clone_repository(git_origin, cwd=destination_directory)


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory"), default=template_directory),
        Argument(name=("-d", "--destination_directory"), default=destination_directory),
        Argument(name=("-n", "--repository_name"), default=repository_name),
        BoolArgument(name=("-r", "--create_repository"), default=create_repository),
        BoolArgument(name=("-c", "--clone_repository"), default=clone_repository),
        BoolArgument(name=("-s", "--store_template"), default=store_template),
        Argument(name=("-l", "--license"), default=license),
        Argument(name=("-a", "--author"), default=author),
        Argument(name=("-y", "--year"), default=year),
        Argument(
            name=("-v", "--repository_visibility"),
            type=check_str_or_int,
            choices=[0, 1, 2, "private", "public", "internal"],
            default=repository_visibility,
        ),
        Argument(name=("-f", "--files"), nargs="+", default=files),
        Argument(name=("-la", "--language"), default=language),
        Argument(
            name=("-p", "--function_patterns"), nargs="+", default=function_patterns
        ),
        Argument(
            name=(
                "-fn",
                "--function_names",
            ),
            nargs="+",
            default=function_names,
        ),
        BoolArgument(name=("-rn", "--replace_name"), default=replace_name),
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    scaffold(**args)


if __name__ == "__main__":
    main()
