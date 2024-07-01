import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import (
    clone_repository,
    get_repository_visibility,
    create_git_repository,
    is_git_repo,
    update_git_repository,
    get_git_origin,
)
from src.licenses import create_license
from src.templates import Template
from utils.file_utils import (
    find_and_replace_in_directory,
)
from utils.str_utils import check_str_or_int
from utils.parser import *
from src.constants import *
import shutil


def scaffold_repository(
    create_repository: bool = create_repository,
    destination_directory: str = destination_directory,
    repository_name: str = repository_name,
    repository_visibility: int = 0,
    author: str = None,
):
    if not create_repository:
        return

    repository_visibility = get_repository_visibility(repository_visibility)
    author = (
        author
        or subprocess.run(
            ["git", "config", "user.name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
    )

    git_origin = get_git_origin(author, repository_name)

    # initialize project directory
    if not (is_git_repo(destination_directory)):
        create_git_repository(git_origin, repository_visibility, repository_name)
        # remove and clone again
        shutil.rmtree(destination_directory, ignore_errors=True)
        clone_repository(git_origin, cwd=os.getcwd())
    else:
        print("Repository already exists. Updating...")
        update_git_repository(git_origin, repository_visibility, author)

    return git_origin


def scaffold(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    repository_name: str = repository_name,
    license: str = license,
    author: str = author,
    year: str = year,
    create_repository: bool = create_repository,
    store_template: bool = store_template,
    repository_visibility: str = repository_visibility,
):
    templ = Template.get_template(template_directory)
    templ: Template

    if templ is None:
        raise ValueError(f"Template '{template_directory}' does not exist.")

    if not repository_name:
        repository_name = os.path.basename(destination_directory)

    # add template to db only if true, else copy it
    if not store_template:
        templ.copy_template(template_directory, destination_directory)
    else:
        templ.add_template(destination_directory)

    create_license(license, destination_directory, author, year)

    # replace all instances of template name with new repository name
    template_name = templ.template_name
    print(f"Replacing all instances of '{template_name}' with '{repository_name}'.")

    find_and_replace_in_directory(
        destination_directory, template_name, repository_name, removed_dirs=[".git"]
    )

    scaffold_repository(
        create_repository,
        destination_directory,
        repository_name,
        repository_visibility,
        author,
    )


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory"), default=template_directory),
        DirectoryArgument(
            name=("-d", "--destination_directory"), default=destination_directory
        ),
        Argument(name=("-n", "--repository_name"), default=repository_name),
        BoolArgument(name=("-c", "--create_repository"), default=create_repository),
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
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    # scaffold(**args)


if __name__ == "__main__":
    main()
