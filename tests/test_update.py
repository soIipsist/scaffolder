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


class TestUpdate(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.function_patterns = languages_metadata.get("Python").get(
            "function_patterns"
        )

        self.update_template_directory = update_template_directory
        self.package_name = "red"
        self.update_destination_directory = update_destination_directory
        self.update_files = update_files

    def get_test_files_dir(self, dirname: str = "dir1", language="python"):
        target_dir = {"python": "python_test_files", "java": "java_test_files"}
        return os.path.join(os.getcwd(), "files", target_dir.get(language), dirname)

    def test_get_functions(self):
        file1 = os.path.join(self.get_test_files_dir(), "file.py")
        print(self.function_patterns)
        funcs = find_functions_in_file(file1, patterns=self.function_patterns)
        print(funcs[6])

    def test_get_updated_functions(self):
        pass

    def test_create_function_patterns(self):
        languages = read_json_file(languages_path)
        languages: dict

        new_languages = languages.copy()

        for key, val in new_languages.items():
            key: dict
            if isinstance(val, dict):
                if not "function_patterns" in val:
                    val.update({"function_patterns": []})
                    print(val)

        overwrite_json_file(languages_path, new_languages)

    def test_update_python(self):
        self.update_files = []
        self.update_template_directory = self.get_test_files_dir()
        self.update_destination_directory = self.get_test_files_dir("dir2")

        print(self.update_template_directory)

        # try with no update files given
        source_files, funcs, updated_content = update(
            self.update_files,
            self.update_template_directory,
            self.update_destination_directory,
        )

    def test_update_java(self):
        self.update_files = []
        self.update_template_directory = self.get_test_files_dir(language="java")
        self.update_destination_directory = self.get_test_files_dir("dir2", "java")

        # try with no update files given
        source_files, funcs, updated_content = update(
            self.update_files,
            self.update_template_directory,
            self.update_destination_directory,
            language="java",
        )


if __name__ == "__main__":
    run_test_methods(TestUpdate.test_create_function_patterns)
