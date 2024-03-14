import os
import subprocess


def get_repository_visibility(repository_visibility: str):
    types = {0: "private", 1: "public", 2: "internal"}

    if isinstance(repository_visibility, int):
        return types.get(repository_visibility, "private")

    return types.get(repository_visibility, "private")

def get_project_name(project_directory:str):
    return os.path.basename(project_directory) if project_directory else None

def create_git_repository(
    project_directory: str,
    create_repository: bool,
    repository_visibility: str,
    git_username: str,
):

    project_name = get_project_name(project_directory)

    if not create_repository:
        return

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
        subprocess.run(args, cwd=project_directory)
