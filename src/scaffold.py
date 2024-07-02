import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.functions import (
    get_function_patterns,
    get_updated_file_content,
    get_updated_functions,
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
from utils.file_utils import find_and_replace_in_directory, find_files
from utils.str_utils import check_str_or_int
from utils.parser import *
from src.constants import *
import shutil


def update_destination_files(
    files: list = [],
    template_directory: str = None,
    destination_directory: str = None,
    language: str = None,
    function_patterns: list = None,
):

    if not files:
        return

    print(
        f'Updating changed files from "{template_directory}" to "{destination_directory}"...'
    )

    # find specified files in source directory

    files = find_files(template_directory, files)

    funcs = []
    updated_content = ""

    for file in files:

        source_file_name = os.path.basename(file)
        dir_name = os.path.dirname(file)

        if dir_name != template_directory:
            base_dir = os.path.basename(os.path.dirname(file))
            update_path = os.path.normpath(
                f"{destination_directory}/{base_dir}/{source_file_name}"
            )
        else:
            update_path = os.path.normpath(
                f"{destination_directory}/{source_file_name}"
            )

        if not is_valid_path(update_path, False):  # file does not exist, copy it
            print(
                f"File '{source_file_name}' not found in '{destination_directory}'. \n Copying to '{update_path}'..."
            )
            subprocess.run(["cp", file, update_path])
        else:
            # get updated content and write it to file
            function_patterns = get_function_patterns(file, language, function_patterns)
            funcs = get_updated_functions(file, update_path, function_patterns)
            content = get_updated_file_content(funcs, update_path)

            with open(update_path, "w", encoding="utf-8") as file:
                file.write(content)

        pp.pprint([f"Source path: {file}", f"Update path: {update_path}"])

    return files, funcs, updated_content


def create_from_template(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    store_template: bool = store_template,
):

    templ = Template.get_template(template_directory)
    templ: Template

    if templ is None:
        raise ValueError(f"Template '{template_directory}' does not exist.")

    # add newly created template to db if store_template is true
    if store_template:
        templ.add_template(destination_directory)
    else:
        templ.copy_template(destination_directory)

    return destination_directory, templ.template_name


def scaffold_repository(
    git_origin: str,
    create_repository: bool = create_repository,
    repository_visibility: int = repository_visibility,
):
    if not create_repository:
        return

    if not is_git_repo(destination_directory):
        create_git_repository(git_origin, repository_visibility)
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
):

    git_origin = get_git_origin(author, repository_name)
    destination_directory, template_name = create_from_template(
        template_directory,
        destination_directory,
        store_template,
    )

    print(f"Replacing all instances of '{template_name}' with '{repository_name}'.")
    find_and_replace_in_directory(
        destination_directory, template_name, repository_name, removed_dirs=[".git"]
    )

    create_license(license, destination_directory, author, year)

    # if files param is specified, make sure to only copy those files
    update_destination_files(
        files, template_directory, destination_directory, language, function_patterns
    )
    return
    scaffold_repository(
        git_origin,
        create_repository,
        repository_visibility,
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
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()

    print(args)
    # scaffold(**args)


if __name__ == "__main__":
    main()
