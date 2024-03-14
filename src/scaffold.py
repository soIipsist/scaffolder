import os
import subprocess
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import get_project_name, get_repository_visibility, create_git_repository
from src.licenses import create_license
from templates.python_template.utils.file_operations import find_and_replace_in_files
from templates.python_template.utils.parser import *
from src.constants import *

def scaffold(
    template_directory: str = template_directory,
    project_directory: str = project_directory,
    license: str = license,
    author: str = author,
    git_username: str = git_username,
    create_repository: bool = create_repository,
    repository_visibility: str = 1,
):

    repository_visibility = get_repository_visibility(repository_visibility)
    git_username = (
        git_username
        or subprocess.run(
            ["git", "config", "user.name"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()
    )

    # initialize project directory
    subprocess.run(["mkdir", project_directory])
    create_license(license, project_directory, author)
    create_template(template_directory, project_directory)

    # create git repository
    create_git_repository(
        project_directory, create_repository, repository_visibility, git_username
    )


def create_template(template_directory: str, project_directory: str):

    project_name = get_project_name(project_directory)

    # copy template directory to project directory
    print(
        "Copying template files from {0} to {1}".format(
            template_directory, project_directory
        )
    )

    command = f"cp -r {template_directory}/* {project_directory}/"
    subprocess.run(command, shell=True)

    # get template project name
    template_name = os.path.split(template_directory)[-1]

    # find and replace all instances of template_name
    find_and_replace_in_files(project_directory, template_name, project_name)


if __name__ == '__main__':
    
    parser_arguments = [
        DirectoryArgument(name=('-t', '--template_directory')),
        DirectoryArgument(name=('-p', '--project_directory')),
        Argument(name=('-l', '--license')),
        Argument(name=('-a', '--author')),
        Argument(name=('-u', '--git_username')),
        Argument(name=('-v', '--repository_visibility'))
    ]
    parser = Parser(parser_arguments)
    
    args = parser.get_command_args()

    scaffold(**args)
    
