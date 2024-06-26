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
        self.update_template_directory = update_template_directory
        self.repository_name = "red"
        self.update_destination_directory = update_destination_directory
        self.update_files = update_files

    def test_get_functions(self):
        file1 = os.path.join(self.get_test_files_dir(), "file.py")
        function_patterns = [
            "['\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:\\s*.*?(?=\\s*def\\s+[\\w_]+\\s*\\([^)]*\\)\\s*:|\\Z)']"
        ]
        funcs = find_functions_in_file(file1, patterns=function_patterns)
        print(funcs[6])

    def test_get_updated_functions(self):
        pass

    def test_get_function_patterns(self):
        # with function patterns not defined
        function_patterns = None
        path = f"{parent_directory}/tests/test_files/test.py"
        language = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        # print(function_patterns)

        # with function patterns defined
        function_patterns = [
            "public\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "public void\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "private\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "protected\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
        ]
        path = f"{parent_directory}/tests/test_files/java.java"
        function_patterns = get_function_patterns(path, language, function_patterns)
        # print(function_patterns)

        # with language defined
        language = "java"
        function_patterns = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        print(function_patterns)


if __name__ == "__main__":
    run_test_methods(TestFunctions.test_get_function_patterns)
