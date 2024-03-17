import os
import subprocess
import shutil

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

    # check if git repo already exists


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
    shutil.rmtree(project_directory, ignore_errors=True)

    target_dir = os.path.dirname(project_directory)
    subprocess.run(['git', 'clone', git_origin], cwd=target_dir)


# def update_git_repository():
#     pass