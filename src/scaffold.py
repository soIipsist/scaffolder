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
        dest_file = os.path.join(destination_directory, rel_path)

        if not os.path.exists(dest_file):
            print(f"Copying from '{file}' to '{dest_file}'")
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


def create_from_template(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    store_template: bool = store_template,
    copy_template: bool = True,
):

    templ = Template.get_template(template_directory)
    templ: Template
    new_templ: Template = None

    if templ is None:
        response = input(
            f"Template '{template_directory}' does not exist.\nWould you like to add it as a template? (y/n)"
        )
        if response in ["yes", "y"]:
            new_templ = Template(template_directory=template_directory)
            new_templ = new_templ.add_template(template_directory, True, False)
        else:
            return None, None

        templ = Template(
            template_directory=template_directory,
            template_name=os.path.basename(destination_directory),
        )

    templ = templ.add_template(destination_directory, store_template, copy_template)
    return destination_directory, templ.template_name


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
    clone_repository: bool = clone_git_repository,
    store_template: bool = store_template,
    repository_visibility: str = repository_visibility,
    files: list = files,
    language: str = language,
    function_patterns: list = function_patterns,
    function_names: list = function_names,
):

    git_origin = get_git_origin(author, repository_name)
    files = find_files(template_directory, files, ["venv"])

    # copy template if files are not defined
    copy_template = len(files) == 0 or not os.path.exists(destination_directory)
    destination_directory, template_name = create_from_template(
        template_directory, destination_directory, store_template, copy_template
    )

    # return
    if destination_directory and template_name:
        update_destination_files(
            template_directory,
            destination_directory,
            language,
            files,
            function_patterns,
            function_names,
        )

        print(license)
        create_license(license, destination_directory, author, year)

        print(f"Replacing all instances of '{repository_name}' with '{template_name}'.")

        return
        find_and_replace_in_directory(
            destination_directory, template_name, repository_name, removed_dirs=[".git"]
        )

        scaffold_repository(
            git_origin, create_repository, repository_visibility, destination_directory
        )

        # clone repository
        if clone_repository:
            shutil.rmtree(destination_directory, ignore_errors=True)
            clone_repository(git_origin, cwd=os.getcwd())


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory"), default=template_directory),
        Argument(name=("-d", "--destination_directory"), default=destination_directory),
        Argument(name=("-n", "--repository_name"), default=repository_name),
        BoolArgument(name=("-c", "--create_repository"), default=create_repository),
        BoolArgument(name=("-cl", "--clone_repository"), default=clone_repository),
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
        Argument(name=("-l", "--language"), default=language),
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
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()

    print(args)
    # scaffold(**args)


if __name__ == "__main__":
    main()
