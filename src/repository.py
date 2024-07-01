import os
import subprocess
from utils.cmd_utils import execute_commands


def get_git_origin(author: str, repository_name: str):
    git_origin = "https://github.com/{0}/{1}.git".format(author, repository_name)
    return git_origin


def get_repository_name(git_origin: str):
    return os.path.basename(git_origin).split(".git")[0]


def get_repository_visibility(repository_visibility: int):
    types = {0: "private", 1: "public", 2: "internal"}

    if isinstance(repository_visibility, str):
        return (
            repository_visibility
            if repository_visibility in types.values()
            else "private"
        )
    if isinstance(repository_visibility, int):
        return types.get(repository_visibility, "private")


def git_repo_exists(repository: str):
    return os.path.exists(os.path.join(repository, ".git"))


def set_repository_visibility(git_origin: str, repository_visibility: str):

    command = f"gh repo edit {git_origin} --visibility {repository_visibility}"
    results = execute_commands([command], return_errors=False)

    if results:
        print(results)

    return repository_visibility


def clone_repository(git_origin: str, cwd: str = None):
    print(f"Cloning {git_origin}.")
    subprocess.run(["git", "clone", git_origin], cwd=cwd)
    return cwd if cwd is not None else os.getcwd()


def rename_repo(git_origin: str, repository_name: str):
    command = f"gh repo rename {repository_name} -R {git_origin} --yes"
    subprocess.run(command, shell=True)

    print(
        f"Renamed repository from {get_repository_name(git_origin)} to {repository_name}."
    )


def create_git_repository(
    git_origin: str,
    repository_name: str,
    repository_visibility: str,
):

    print(f"Creating git repository: {git_origin}")

    repository_visibility = get_repository_visibility(repository_visibility)
    repository_visibility = "--{0}".format(repository_visibility)

    print(repository_visibility)
    commands = [
        ["gh", "repo", "create", repository_name, repository_visibility],
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
            subprocess.run(args, check=True)
        except Exception as e:
            print(e)

    return git_origin


def update_git_repository(
    git_origin: str,
    destination_directory: str,
    repository_visibility: int = 0,
):

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "commit"],
        ["git", "push", "-u", "origin", "main"],
    ]
    # check if there were any changes
    output = subprocess.run(
        ["git", "diff", "--name-status"], capture_output=True, text=True
    )

    if output.stdout:
        for command in commands:
            try:
                subprocess.run(command, cwd=destination_directory)
            except Exception as e:
                print(e)

    set_repository_visibility(git_origin, repository_visibility)
    print("Update completed.")


def delete_git_repository(git_origin: str):
    try:
        command = ["gh", "repo", "delete", f"{git_origin}", "--yes"]
        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Successfully deleted the repository {git_origin} on GitHub.")
        else:
            print(f"Error deleting repository: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")
