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

    def test_get_function_patterns(self):
        # with function patterns not defined
        function_patterns = None
        path = self.get_file("main.py", "python_test_files")

        language = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        # print(function_patterns)

        # with function patterns defined
        function_patterns = [
            "public\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
        ]
        path = self.get_file("file.java", "java_test_files")
        function_patterns = get_function_patterns(path, language, function_patterns)

        # with language defined
        language = "java"
        function_patterns = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        print(function_patterns)

    def test_find_java_functions(self):
        file = self.get_file("file.java", "java_test_files")
        function_patterns = [
            "['\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:|\\Z)']"
        ]
        funcs = find_functions_in_file(file, patterns=function_patterns)
        print(funcs)

    def test_find_python_functions(self):
        pass

    def test_update_function_patterns(self):
        from utils.sqlite import bad_inputs

        patterns = {
            "java": bad_inputs[-3],
        }

        for k, v in patterns.items():
            lang = Language(k, function_patterns=v)
            lang.update()


if __name__ == "__main__":
    run_test_methods(TestFunctions.test_update_function_patterns)
