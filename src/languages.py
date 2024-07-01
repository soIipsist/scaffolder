import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.parser import Argument, Parser, SubCommand, PathArgument
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

    def get_description(self):
        return f"Language: {self.language}\nExtensions: {self.extensions}\nFunction patterns: {self.function_patterns}"

    def add_language(self):
        insert_id = self.insert()

        if not insert_id:
            insert_id = self.update()

        if insert_id:
            print(f"Language {self.language} was inserted successfully.")

    def delete_language(self):
        self.delete()
        print(f"Language {self.language} was deleted successfully.")

    def get_language(self, extension: str):
        filter_condition = (
            f"language = {self.language} OR extensions LIKE %'{extension}'%"
        )
        items = self.select(filter_condition)
        return items[0] if len(items) > 0 else None

    def __repr__(self) -> str:
        return self.get_description()

    def __str__(self) -> str:
        return self.get_description()


def detect_language(file_path: str):

    from src.constants import languages

    if not languages:
        languages = Language().select_all()

    extension = get_file_extension(file_path)

    for language in languages:
        language: Language
        if extension in language.extensions:
            return language.language

    return "python"


def import_languages(languages_json: str = None):
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


def main():
    parser_arguments = [
        Argument(name=("-l", "--language"), default=None),
        Argument(name=("-e", "--extension"), default=None),
    ]
    add_arguments = [
        Argument(name=("-l", "--language"), default=None),
        Argument(name=("-e", "--extensions"), default=[], nargs="+"),
        Argument(name=("-f", "--function_patterns"), default=[], nargs="+"),
    ]

    delete_arguments = [
        Argument(name=("-l", "--language")),
    ]

    import_arguments = [PathArgument(name=("-l", "--languages_json"))]

    subcommands = [
        SubCommand("add", add_arguments),
        SubCommand("delete", delete_arguments),
        SubCommand("import", import_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)
    args = parser.get_command_args()
    language_args = parser.get_callable_args(Language.__init__)
    language = Language(**language_args)

    cmd_dict = {
        "add": language.add_language,
        "delete": language.delete_language,
        "import": import_languages,
    }
    func = parser.get_command_function(cmd_dict)

    if not func:
        language.language = args.get("language", None)
        language = language.get_language(args.get("extension"))
        print(language)
    else:
        args = parser.get_callable_args(func)
        func(**args)


if __name__ == "__main__":
    main()
