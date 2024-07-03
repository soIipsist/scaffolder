import os
from pprint import pp
import re
import subprocess
from utils.file_utils import find_files, read_file
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


def get_updated_functions(source_path: str, dest_path: str, patterns: list):
    """
    Return functions dictionary based on type (modified, added or removed).
    """
    added_functions = []
    modified_functions = []
    replaced_functions = []

    funcs1 = find_functions_in_file(source_path, patterns)
    funcs2 = find_functions_in_file(dest_path, patterns)

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


def get_function_names(funcs: dict, names: list = []):
    """Return functions that contain the strings specified."""
    if not names:
        return funcs

    for key, val in funcs.items():
        new_val = []

        for name in names:
            for v in val:
                match = re.match(f"(.*?){name}\\((.*?)\\)", v)
                if match:
                    new_val.append(v)

        funcs[key] = new_val
    return funcs
