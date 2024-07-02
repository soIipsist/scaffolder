import os
from pprint import pp
import re
import subprocess
from utils.file_utils import read_file
from utils.path_utils import is_valid_path


def get_function_patterns(
    file_path: str, language: str = None, function_patterns: list = None
):
    from src.languages import detect_language, Language

    if function_patterns:
        return function_patterns

    if not language:
        language = detect_language(file_path)

    default_patterns = ["\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def|\\Z)"]

    lang = Language(language=language).select()

    if len(lang) > 0:
        function_patterns = getattr(lang[0], "function_patterns")
        return function_patterns if function_patterns else default_patterns


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


def update(
    files: list = [],
    update_template_directory: str = None,
    update_destination_directory: str = None,
    language: str = None,
    function_patterns: list = None,
):

    if not files:
        files = [file for file in os.listdir(update_template_directory)]

    print(
        f'Updating changed files from "{update_template_directory}" to "{update_destination_directory}"...'
    )

    # find specified files in source directory

    source_files = find_files(update_template_directory, files)
    update_template_directory = os.path.normpath(update_template_directory)
    update_destination_directory = os.path.normpath(update_destination_directory)

    funcs = []
    updated_content = ""

    for source_path in source_files:

        source_file_name = os.path.basename(source_path)
        dir_name = os.path.dirname(source_path)

        if dir_name != update_template_directory:
            base_dir = os.path.basename(os.path.dirname(source_path))
            update_path = os.path.normpath(
                f"{update_destination_directory}/{base_dir}/{source_file_name}"
            )
        else:
            update_path = os.path.normpath(
                f"{update_destination_directory}/{source_file_name}"
            )

        if not is_valid_path(update_path, False):  # file does not exist, copy it
            print(
                f"File '{source_file_name}' not found in '{update_destination_directory}'. \n Copying to '{update_path}'..."
            )
            subprocess.run(["cp", source_path, update_path])
        else:
            # get updated content and write it to file
            function_patterns = get_function_patterns(
                source_path, language, function_patterns
            )
            funcs = get_updated_functions(source_path, update_path, function_patterns)
            content = get_updated_file_content(funcs, update_path)

            with open(update_path, "w", encoding="utf-8") as file:
                file.write(content)

        pp.pprint([f"Source path: {source_path}", f"Update path: {update_path}"])

    return source_files, funcs, updated_content
