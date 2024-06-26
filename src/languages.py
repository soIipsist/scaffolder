import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.sqlite_connection import *
from utils.sqlite_item import *
from data.sqlite_data import *

from utils.file_utils import read_and_parse_file, get_file_extension


class Language(SQLiteItem):
    language: str
    extensions: list
    function_patterns: list = []

    def __init__(
        self,
        language: str = None,
        extensions: list = [],
        function_patterns: list = [],
    ) -> None:
        super().__init__(table_values=language_values)
        self.language = language
        self.extensions = extensions
        self.function_patterns = function_patterns
        self.filter_condition = f"language = {self.language}"


def detect_language(file_path: str, languages: list = None):

    if not languages:
        languages = Language().select_all()

    extension = get_file_extension(file_path)

    for language in languages:
        language: Language
        if extension in language.extensions:
            key: str
            return key.lower()

    return "python"


def add_languages(languages_json: str = None):
    if not languages_json:
        languages_json = os.path.join(parent_directory, "data", "languages.json")

    languages = read_and_parse_file(languages_json)
    languages: dict

    print("Adding languages...")

    for key, value in languages.items():
        key: str
        lang_extensions = value.get("extensions", [])

        if lang_extensions is None:
            lang_extensions = []
        extensions = [str(extension).removeprefix(".") for extension in lang_extensions]

        new_lang = Language(
            language=key.lower(),
            extensions=extensions,
            function_patterns=value.get("function_patterns"),
        )

        new_lang.insert()


if __name__ == "__main__":
    create_db(db_path, tables, values)
    add_languages()
