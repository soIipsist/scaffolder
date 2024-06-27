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
        self.update_template_directory = update_template_directory
        self.repository_name = "red"
        self.update_destination_directory = update_destination_directory
        self.update_files = update_files

    def test_update_python(self):
        self.update_files = []
        self.update_template_directory = self.get_files_directory(
            "sample_test_files", "original_dir"
        )
        self.update_destination_directory = self.get_files_directory(
            "sample_test_files", "updated_dir"
        )

        print(self.update_template_directory)

        # try with no update files given
        source_files, funcs, updated_content = update(
            self.update_files,
            self.update_template_directory,
            self.update_destination_directory,
        )

    def test_update_java(self):
        self.update_files = []

        # try with no update files given
        source_files, funcs, updated_content = update(
            self.update_files,
            self.update_template_directory,
            self.update_destination_directory,
            language="java",
        )


if __name__ == "__main__":
    run_test_methods(TestUpdate.test_update_java)
