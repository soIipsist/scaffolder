import os
import subprocess
import shutil

from templates.python_template.utils.dictionary_operations import invert_dict


def get_repository_visibility(repository_visibility: int):
    types = {0: "private", 1: "public", 2: "internal"}

    if isinstance(repository_visibility, str):
        types = invert_dict(types)
        return repository_visibility if repository_visibility in types else "private"

    return types.get(repository_visibility, "private")


def create_git_repository(
    project_directory: str,
    repository_visibility: str,
    git_username: str,
):

    project_name = os.path.basename(project_directory)

    git_origin = "https://github.com/{0}/{1}.git".format(git_username, project_name)
    print(f"Creating git repository: {git_origin}")

    repo_visibility = "--{0}".format(repository_visibility)

    commands = [
        ["gh", "repo", "create", project_name, repo_visibility],
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m", "published branch"],
        ["git", "branch", "-M", "main"],
        ["git", "status"],
        ["git", "remote", "remove", "origin"],
        ["git", "remote", "add", "origin", git_origin],
        ["git", "remote", "-v"],
        ["git", "push", "-u", "origin", "main"],
    ]

    for args in commands:

        try:
            subprocess.run(args, cwd=project_directory, check=True)
        except Exception as e:
            print(e)

    # remove and clone again
    clone_repository(project_directory, git_origin)


def clone_repository(project_directory: str, git_origin: str):
    # remove and clone again
    shutil.rmtree(project_directory, ignore_errors=True)
    target_dir = os.path.dirname(project_directory)
    subprocess.run(["git", "clone", git_origin], cwd=target_dir)


def git_repo_exists(project_directory: str):
    return os.path.exists(os.path.join(project_directory, ".git"))


def update_git_repository(project_directory: str):

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "commit"],
        ["git", "push", "-u", "origin", "main"],
    ]
    # check if there were any changes
    output = subprocess.run(
        ["git", "diff", "--name-status"],
        capture_output=True,
        text=True,
        cwd=project_directory,
    )

    if output.stdout:
        for command in commands:
            try:
                subprocess.run(command, cwd=project_directory)
            except Exception as e:
                print(e)

    print("Update completed.")


def rename_repo(project_directory: str, repository_name: str, host: str):
    if not (git_repo_exists(project_directory)):
        return
    original_name = os.path.basename(project_directory)

    command = f"gh repo rename {repository_name} -R {host}/{original_name} --yes"
    subprocess.run(command, shell=True)

    print(f"Renamed repository from {original_name} to {repository_name}.")
