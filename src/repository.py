import os
import subprocess
from utils.dict_utils import invert_dict


def get_repository_visibility(repository_visibility: int):
    types = {0: "private", 1: "public", 2: "internal"}

    if isinstance(repository_visibility, str):
        types = invert_dict(types)
        return repository_visibility if repository_visibility in types else "private"

    return types.get(repository_visibility, "private")


def set_repository_visibility(
    repository_name: str, repository_visibility: str, author: str
):

    command = (
        f"gh repo edit {author}/{repository_name} --visibility {repository_visibility}"
    )
    subprocess.run(command, shell=True)

    return repository_visibility


def create_git_repository(
    repository_name: str,
    repository_visibility: str,
    author: str,
):

    git_origin = "https://github.com/{0}/{1}.git".format(author, repository_name)
    print(f"Creating git repository: {git_origin}")

    repo_visibility = "--{0}".format(repository_visibility)

    commands = [
        ["gh", "repo", "create", repository_name, repo_visibility],
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


def clone_repository(destination_directory: str, git_origin: str):
    print(f"Cloning {destination_directory}")
    target_dir = os.path.dirname(destination_directory)
    subprocess.run(["git", "clone", git_origin], cwd=target_dir)


def git_repo_exists(repository: str):
    return os.path.exists(os.path.join(repository, ".git"))


def update_git_repository(
    destination_directory: str,
    repository_name: str = None,
    repository_visibility: int = "public",
    author: str = None,
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

    set_repository_visibility(repository_name, repository_visibility, author)
    print("Update completed.")


def rename_repo(original_name: str, repository_name: str, author: str):
    command = f"gh repo rename {repository_name} -R {author}/{original_name} --yes"
    subprocess.run(command, shell=True)

    print(f"Renamed repository from {original_name} to {repository_name}.")


def delete_git_repository(repository_name: str, author: str):
    try:
        command = ["gh", "repo", "delete", f"{author}/{repository_name}", "--yes"]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode == 0:
            print(
                f"Successfully deleted the repository {author}/{repository_name} on GitHub."
            )
        else:
            print(f"Error deleting repository: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")
