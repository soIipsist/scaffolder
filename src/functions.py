import os
import re
from utils.file_utils import read_file


def find_files(directory: str, file_names: list):
    """
    Given an array of file names, return a list of valid file paths.
    """

    files = []

    for root, dirs, directory_files in os.walk(directory):
        for file in directory_files:
            file_path = os.path.join(root, file)
            normalized_path = os.path.normpath(file_path)
            base_name = os.path.basename(file_path)

            # Check if the file path or base name matches any in the array
            if file_path in file_names or base_name in file_names:
                files.append(normalized_path)

    return set(files)


def find_functions_in_file(file_path: str, patterns: list):
    """Given a list of patterns, return functions of a file."""

    file_content = read_file(file_path)

    functions = []

    matches = []

    for pattern in patterns:
        matches.extend(re.finditer(pattern, file_content, re.MULTILINE | re.DOTALL))

    for match in matches:
        function = match.group(0)  # Use group(0) to get the entire match
        functions.append(function.strip())
    return functions


def get_function_prefixes(functions: list):
    """
    Return all function prefixes from list.
    """

    return [func.strip().split("\n")[0] for func in functions]


def get_updated_functions(source_path: str, update_path: str, patterns: list):
    """
    Return functions dictionary based on type (modified, added or removed).
    """
    added_functions = []
    modified_functions = []
    replaced_functions = []

    funcs1 = find_functions_in_file(source_path, patterns)
    funcs2 = find_functions_in_file(update_path, patterns)

    diff_functions = list(set(funcs1).difference(funcs2))

    func1_prefixes = get_function_prefixes(funcs1)
    func2_prefixes = get_function_prefixes(funcs2)

    modified_prefixes = []

    for func in diff_functions:
        prefix = func.strip().split("\n")[0]

        if prefix in func1_prefixes and prefix in func2_prefixes:
            modified_prefixes.append(prefix)
            modified_functions.append(func)
        else:
            added_functions.append(func)

    for func in funcs2:
        prefix = func.strip().split("\n")[0]
        if prefix in func2_prefixes and prefix in modified_prefixes:
            replaced_functions.append(func)

    functions = {
        "added": added_functions,
        "modified": modified_functions,
        "replaced": replaced_functions,
    }

    return functions


def get_updated_file_content(functions: dict, update_path: str):
    """Return content of an updated file (a file with functions from a previous source)."""

    if not isinstance(functions, dict):
        raise (ValueError("'functions' must be a dictionary."))

    # update file2 with functions of func1
    updated_content = read_file(update_path)

    added_functions = functions.get("added", [])
    modified_functions = functions.get("modified", [])
    replaced_functions = functions.get("replaced", [])

    for modified_func, replaced_func in zip(modified_functions, replaced_functions):
        updated_content = updated_content.replace(replaced_func, modified_func)

    for func in added_functions:
        updated_content += "\n\n" + func

    return updated_content


# def get_function_names(updated_content, patterns):
#     """ Return function names from updated content. """

#     function_names = []

#     for u in updated_content.splitlines():
#         for pattern in patterns:
#             match = re.match(pattern, u)

#             if match:
#                 function_names.append(match.group(0))


#     return updated_content
