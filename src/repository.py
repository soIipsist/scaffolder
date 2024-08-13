import os
import subprocess
from utils.cmd_utils import execute_commands


def get_git_origin(author: str, repository_name: str):
    git_origin = "https://github.com/{0}/{1}.git".format(author, repository_name)
    return git_origin


def get_author(author: str = None):
    if not author:
        results = execute_commands([["git", "config", "user.name"]])

        if len(results) > 0:
            return results[0].stdout
    return author


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


def is_git_repo(repository: str):
    results = execute_commands([["git", "status"]], cwd=repository)
    return results and results[0].stdout.strip() == repository


def set_repository_visibility(git_origin: str, repository_visibility: str):

    repository_visibility = get_repository_visibility(repository_visibility)
    command = f"gh repo edit {git_origin} --visibility {repository_visibility}"
    results = execute_commands([command], return_errors=False)

    if results:
        print(
            f"Repository visibility for {git_origin} was set to {repository_visibility}."
        )

    return repository_visibility


def clone_git_repository(git_origin: str, cwd: str = None):
    print(f"Cloning {git_origin}.")
    subprocess.run(["git", "clone", git_origin], cwd=cwd)
    return cwd if cwd is not None else os.getcwd()


def ignore_git_files(directory, files):
    return [f for f in files if f == ".git"]


def rename_repo(git_origin: str, repository_name: str):
    command = f"gh repo rename {repository_name} -R {git_origin} --yes"
    subprocess.run(command, shell=True)

    print(
        f"Renamed repository from {get_repository_name(git_origin)} to {repository_name}."
    )


def create_git_repository(
    git_origin: str,
    repository_visibility: str,
    cwd: str = None,
):

    print(f"Creating git repository: {git_origin}")

    repository_visibility = get_repository_visibility(repository_visibility)
    repository_visibility = "--{0}".format(repository_visibility)

    repository_name = get_repository_name(git_origin)

    commands = [
        [
            "gh",
            "repo",
            "create",
            repository_name,
            repository_visibility,
        ],
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

    results, errors = execute_commands(commands, return_errors=True, cwd=cwd)

    if results:
        print(f"{git_origin} was created successfully.")

    if errors:
        for error in errors:
            print("An error occured: ", error.stderr, error.output, error)
    return git_origin


def git_diff(cwd: str = None):
    result = execute_commands(["git diff --name-status"], cwd=cwd)
    if result:
        result = result[0].stdout
        return result


def update_git_repository(
    git_origin: str,
    repository_visibility: int = 0,
    cwd: str = None,
):
    print(f"Repository {git_origin} already exists. Updating...")

    commands = [
        ["git", "add", "."],
        ["git", "commit", "-m", "commit"],
        ["git", "push", "-u", "origin", "main"],
    ]

    diff = git_diff(cwd)

    if diff:
        results = execute_commands(commands, cwd=cwd)
        if results:
            print(f"{git_origin} was updated successfully.")
            set_repository_visibility(git_origin, repository_visibility)

    return git_origin


def delete_git_repository(git_origin: str, cwd: str = None):
    commands = [f"gh repo delete {get_repository_name(git_origin)} --yes"]
    results, errors = execute_commands(commands, return_errors=True, cwd=cwd)

    if results:
        result = results[0]
        if result.returncode == 0:
            print(f"Successfully deleted the repository {git_origin} on GitHub.")
            return git_origin
        else:
            print(f"Error deleting repository: {result.stderr}")
    else:
        for error in errors:
            print(error.stderr)
