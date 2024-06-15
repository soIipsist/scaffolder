import os
from pathlib import Path


def is_valid_dir(path, raise_error=True):
    """
    Returns a directory if it's valid.
    """

    if os.path.isdir(path):
        return path
    else:
        if raise_error:
            raise NotADirectoryError(path)


def is_valid_path(path, raise_error=True):
    """
    Returns a path if it's valid.
    """

    if not os.path.exists(path):
        if raise_error:
            raise FileNotFoundError(path)
        return None
    return path


def path_to_package(file_path: str, package_name: str = ""):
    """
    Converts a file path to a package name and returns the resource name.
    """

    path = Path(file_path).resolve()

    if package_name:
        package_name = Path(package_name).resolve()
    else:
        package_name = Path().resolve()

    # Find the index of the base_dir in the resolved file path
    try:
        index = path.parts.index(package_name.name)
    except ValueError:
        raise ValueError(
            f"Base directory '{package_name}' not found in path '{file_path}'"
        )

    # Get the relative path starting from the base_dir
    relative_path = Path(*path.parts[index + 1 :])

    package_path = relative_path.parent
    package_name = ".".join(package_path.parts)
    resource_name = path.name

    return package_name, resource_name
