import os
import subprocess
import shutil

from utils.dict_utils import invert_dict


def get_repository_visibility(repository_visibility: int):
    types = {0: "private", 1: "public", 2: "internal"}

    if isinstance(repository_visibility, str):
        types = invert_dict(types)
        return repository_visibility if repository_visibility in types else "private"

    return types.get(repository_visibility, "private")


def set_repository_visibility(
    destination_directory: str, repository_visibility: str, author: str
):

    repository_name = os.path.basename(destination_directory)
    command = (
        f"gh repo edit {author}/{repository_name} --visibility {repository_visibility}"
    )
    subprocess.run(command, shell=True)


def create_git_repository(
    destination_directory: str,
    repository_visibility: str,
    git_username: str,
):

    project_name = os.path.basename(destination_directory)

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
            subprocess.run(args, cwd=destination_directory, check=True)
        except Exception as e:
            print(e)

    # remove and clone again
    clone_repository(destination_directory, git_origin)


def clone_repository(destination_directory: str, git_origin: str):
    # remove and clone again
    shutil.rmtree(destination_directory, ignore_errors=True)
    target_dir = os.path.dirname(destination_directory)
    subprocess.run(["git", "clone", git_origin], cwd=target_dir)


def git_repo_exists(destination_directory: str):
    return os.path.exists(os.path.join(destination_directory, ".git"))


def update_git_repository(
    destination_directory: str, repository_visibility: int, git_username: str
):

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
        cwd=destination_directory,
    )

    if output.stdout:
        for command in commands:
            try:
                subprocess.run(command, cwd=destination_directory)
            except Exception as e:
                print(e)

    set_repository_visibility(
        destination_directory, repository_visibility, git_username
    )
    print("Update completed.")


def rename_repo(destination_directory: str, repository_name: str, author: str):
    if not (git_repo_exists(destination_directory)):
        return
    original_name = os.path.basename(destination_directory)

    command = f"gh repo rename {repository_name} -R {author}/{original_name} --yes"
    subprocess.run(command, shell=True)

    print(f"Renamed repository from {original_name} to {repository_name}.")


def delete_repository(destination_directory: str, repository_name: str, author: str):
    try:
        # Construct the gh command to delete the repository
        command = ["gh", "repo", "delete", f"{author}/{repository_name}", "--confirm"]

        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors
        if result.returncode == 0:
            print(
                f"Successfully deleted the repository {author}/{repository_name} on GitHub."
            )
        else:
            print(f"Error deleting repository: {result.stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")
