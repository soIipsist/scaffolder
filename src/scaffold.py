import os
import subprocess
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from src.repository import get_repository_visibility, create_git_repository, git_repo_exists, update_git_repository
from src.licenses import create_license
from src.templates import get_template_directory
from templates.python_template.utils.file_operations import find_and_replace_in_directory
from templates.python_template.utils.parser import *
from src.constants import *

def scaffold(
    template: str = template_directory,
    project_directory: str = project_directory,
    license: str = license,
    author: str = author,
    git_username: str = git_username,
    create_repository: bool = create_repository,
    repository_visibility: str = 1,
):
    template_directory = get_template_directory(template)

    if not os.path.exists(project_directory):
        subprocess.run(["mkdir", project_directory], errors=None)
        create_license(license, project_directory, author)
        create_template(template_directory, project_directory)

    if not create_repository:
        return
    
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
    if not(git_repo_exists(project_directory)):

        # create git repository
        create_git_repository(
            project_directory, repository_visibility, git_username
        )
    else:
        print('Project already exists. Updating...')
        update_git_repository(project_directory)


def create_template(template_directory: str, project_directory: str):

    project_name = os.path.basename(project_directory) 

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
    find_and_replace_in_directory(project_directory, template_name, project_name)


if __name__ == '__main__':
    
    parser_arguments = [
        Argument(name=('-t', '--template')),
        DirectoryArgument(name=('-p', '--project_directory')),
        Argument(name=('-l', '--license')),
        Argument(name=('-a', '--author')),
        Argument(name=('-u', '--git_username')),
        Argument(name=('-v', '--repository_visibility'))
    ]
    parser = Parser(parser_arguments)
    
    args = parser.get_command_args()

    scaffold(**args)
    
