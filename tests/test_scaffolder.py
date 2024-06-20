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

from utils.file_utils import overwrite_file

licenses = ["mit", "afl-3.0"]
target_directory = os.getcwd()
author = "soIipsist"


class TestScaffolder(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.template_directory = template_directory
        self.destination_directory = destination_directory
        self.license = license
        self.author = author
        self.author = author
        self.create_repository = create_repository
        self.repository_visibility = repository_visibility

        self.test_files_dir = self.get_test_files_dir()
        self.test_files_dir_2 = self.get_test_files_dir("dir2")

    def get_test_files_dir(self, dirname: str = "dir1", language="python"):
        target_dir = {"python": "python_test_files", "java": "java_test_files"}
        return os.path.join(os.getcwd(), target_dir.get(language), dirname)

    def test_get_files_dir(self):
        dir1 = self.get_test_files_dir()
        print(dir1)
        self.assertTrue(os.path.exists(dir1))

        dir2 = self.get_test_files_dir("dir2")
        print(dir2)
        self.assertTrue(os.path.exists(dir2))

    def test_scaffold_local(self):
        self.create_repository = False
        self.repository_visibility = 0
        scaffold(
            self.template_directory,
            self.destination_directory,
            self.repository_name,
            self.license,
            self.author,
            self.author,
            self.create_repository,
            self.repository_visibility,
        )
        # self.assertTrue(os.path.exists(self.destination_directory))

    def test_scaffold(self):
        self.template_directory = self.gettem
        self.create_repository = True
        self.repository_visibility = 1
        scaffold(
            self.template_directory,
            self.destination_directory,
            self.repository_name,
            self.license,
            self.author,
            self.author,
            self.create_repository,
            self.repository_visibility,
        )

    def test_detect_language(self):
        file_path = ""
        with self.assertRaises(FileNotFoundError):
            detect_language(file_path)

        file_path = f"{parent_directory}/tests/test_files/test.py"
        java_path = f"{parent_directory}/tests/test_files/java.java"

        self.assertTrue(detect_language(file_path) == "python")
        self.assertTrue(detect_language(java_path) == "java")
        print(detect_language(java_path))

    def test_get_function_patterns(self):
        # with function patterns not defined
        function_patterns = None
        path = f"{parent_directory}/tests/test_files/test.py"
        language = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        print(function_patterns)

        # with function patterns defined
        function_patterns = [
            "public\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "public void\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "private\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
            "protected\\s*(\\w+\\s+\\w+\\s*\\([^)]*\\))\\s*\\{[^}]*\\}",
        ]
        path = f"{parent_directory}/tests/test_files/java.java"
        function_patterns = get_function_patterns(path, language, function_patterns)
        print(function_patterns)

        # with language defined
        language = "java"
        function_patterns = None
        function_patterns = get_function_patterns(path, language, function_patterns)
        print(function_patterns)


if __name__ == "__main__":
    run_test_methods(TestScaffolder.test_get_function_patterns)
