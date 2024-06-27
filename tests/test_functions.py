import unittest
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from tests.test_base import TestBase, run_test_methods

from src.scaffold import *
from src.update import *
from src.settings import *
from src.licenses import *
from src.templates import *
from src.constants import *
from src.functions import find_functions_in_file

from utils.file_utils import overwrite_file

licenses = ["mit", "afl-3.0"]
target_directory = os.getcwd()
author = "soIipsist"


class TestFunctions(TestBase):
    def setUp(self) -> None:
        super().setUp()

        self.c_patterns = [
            "\\s*\\w[\\w\\s\\*]*\\s+\\w+\\s*\\([^)]*\\)\\s*(\\{[^}]*\\}|;|$)"
        ]
        self.cpp_patterns = [
            "\\s*(public|protected|private|virtual|static|inline|const|template<[^>]+>)?\\s*[\\w\\<\\>\\*\\&\\:\\~\\s]+\\s*\\w+\\s*\\([^)]*\\)\\s*(const)?\\s*(\\{[^}]*\\}|;|$)"
        ]
        self.go_patterns = ["\\s*func\\s*\\([^)]*\\)\\s*(\\w)*\\{[^{}]*\\}"]

        self.cs_patterns = []

        self.python_patterns = [
            "\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:|\\Z)"
        ]
        self.java_patterns = [
            "\\s*(public|protected|private|static|final|native|synchronized|abstract|transient|volatile|\\s)*\\s*[\\w\\<\\>\\[\\]]+\\s+[\\w_]+\\s*\\([^)]*\\)\\s*(\\{.*?\\}|;)"
        ]
        self.javascript_patterns = [
            "\\s*(const|export|let|\\s)*\\s*[\\w_]+\\s*=\\s*(async\\s*)*\\([^)]*\\)\\s*=>\\s*[^;]+;"
        ]

    def test_get_function_patterns(self):
        # with function patterns not defined
        function_patterns = None
        path = self.get_file("file.py", "language_test_files")

        language = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        # print(function_patterns)

        # with no language defined
        path = self.get_file("file.java", "language_test_files")
        function_patterns = get_function_patterns(path, language, self.java_patterns)

        # with language defined
        language = "java"
        function_patterns = None
        function_patterns = get_function_patterns(path, language, self.java_patterns)
        print(function_patterns)

    def find_functions(self, lang="java", patterns=None):
        lang = Language(language=lang).select()[0]

        lang: Language
        file = self.get_file(f"file.{lang.extensions[0]}", "language_test_files")
        patterns = lang.function_patterns if patterns is None else patterns
        funcs = find_functions_in_file(file, patterns=patterns)
        return funcs

    def test_find_functions(self):
        langs = {
            "c": self.c_patterns,
            "c++": self.cpp_patterns,
            "python": self.python_patterns,
            "java": self.java_patterns,
            "javascript": self.javascript_patterns,
            "go": self.go_patterns,
            "c#": self.cs_patterns,
        }

        for k, v in langs.items():
            funcs = self.find_functions(k, v)
            print(k, ": ", len(funcs))

            # if k == "go":
            #     print(funcs)

    def test_update_function_patterns(self):

        patterns = {"java": self.java_patterns, "python": self.python_patterns}

        for k, v in patterns.items():
            lang = Language(k, function_patterns=v)
            lang = lang.select()

            if lang:
                lang = lang[0]
                lang: Language
                lang.function_patterns = v
                lang.update()


if __name__ == "__main__":
    run_test_methods(TestFunctions.test_find_functions)
