import os
import subprocess

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import (
    clone_repository,
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
import shutil


def scaffold(
    template_directory: str = template_directory,
    destination_directory: str = destination_directory,
    repository_name: str = repository_name,
    license: str = license,
    author: str = author,
    year: str = year,
    create_repository: bool = create_repository,
    repository_visibility: str = repository_visibility,
):
    templ = get_template(template_directory)

    if templ is None:
        raise ValueError(f"Template '{template_directory}' does not exist.")

    # copy template first
    templ.copy_template(template_directory, destination_directory)
    create_license(license, destination_directory, author, year)

    # replace all instances of template name with new repository name
    template_name = templ.template_name

    if not template_name:
        template_name = os.path.basename(templ.template_directory)

    print(f"Replacing all instances of '{template_name}' with '{repository_name}'.")

    find_and_replace_in_directory(
        destination_directory, template_name, repository_name, removed_dirs=[".git"]
    )

    if create_repository:
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

        cwd = os.getcwd()
        os.chdir(destination_directory)

        # initialize project directory
        if not (git_repo_exists(destination_directory)):
            git_origin = create_git_repository(
                repository_name, repository_visibility, author
            )
            # remove and clone again
            shutil.rmtree(destination_directory, ignore_errors=True)
            clone_repository(destination_directory, git_origin)
        else:
            print("Repository already exists. Updating...")
            update_git_repository(repository_name, repository_visibility, author)

        os.chdir(cwd)


def main():

    parser_arguments = [
        Argument(name=("-t", "--template_directory")),
        DirectoryArgument(name=("-d", "--destination_directory")),
        Argument(name=("-n", "--repository_name")),
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
