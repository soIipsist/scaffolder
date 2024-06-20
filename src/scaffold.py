import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import (
    get_repository_visibility,
    create_git_repository,
    git_repo_exists,
    update_git_repository,
    rename_repo,
)
from src.licenses import create_license
from src.templates import Template, get_template
from utils.file_utils import (
    find_and_replace_in_directory,
)
from utils.parser import *
from src.constants import *


def scaffold(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    package_name: str = package_name,
    license: str = license,
    author: str = author,
    year: str = year,
    create_repository: bool = create_repository,
    repository_visibility: str = repository_visibility,
):
    templ = get_template(template_directory)
    print(templ)

    return
    create_template(template_directory, destination_directory)

    # find and replace all instances of template_name
    find_and_replace_in_directory(
        destination_directory, template_name, package_name, removed_dirs=[".git"]
    )

    if not os.path.exists(destination_directory):
        subprocess.run(["mkdir", destination_directory], errors=None)
    else:
        # path already exists, so update based on metadata
        if package_name:
            original_name = os.path.basename(destination_directory)
            rename_repo(destination_directory, package_name, author)

    if not create_repository:
        return

    create_license(license, destination_directory, author, year)

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

    # initialize project directory
    if not (git_repo_exists(destination_directory)):
        create_git_repository(destination_directory, repository_visibility, author)
    else:
        print("Project already exists. Updating...")
        update_git_repository(destination_directory, repository_visibility, author)


def create_template(template: Template, destination_directory: str):

    # copy template directory to project directory
    template.copy_template(template.template_directory, destination_directory)

    # get template project name
    template_name = os.path.split(template_directory)[-1]


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory")),
        DirectoryArgument(name=("-d", "--destination_directory")),
        Argument(name=("-n", "--package_name")),
        BoolArgument(name=("-c", "--create_repository")),
        Argument(name=("-l", "--license")),
        Argument(name=("-a", "--author")),
        Argument(name=("-y", "--year")),
        Argument(name=("-v", "--repository_visibility"), type=int, choices=[0, 1, 2]),
    ]
    parser = Parser(parser_arguments)

    args = parser.get_command_args()

    scaffold(**args)


if __name__ == "__main__":
    main()
