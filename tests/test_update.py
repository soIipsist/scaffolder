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

    def get_test_files_dir(self, dirname: str = "dir1", language="python"):
        target_dir = {"python": "python_test_files", "java": "java_test_files"}
        return os.path.join(os.getcwd(), target_dir.get(language), dirname)

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


if __name__ == "__main__":
    run_test_methods(TestUpdate.test_create_function_patterns)
