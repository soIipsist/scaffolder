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


class TestSettings(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.parameters = ["template_directory", "license"]

    def test_list_settings(self):
        settings = list_settings(self.parameters)
        self.assertIsNotNone(settings)
        self.assertListEqual(list(settings.keys()), self.parameters)

    def test_update_settings(self):
        update_settings({"template_directory": "gaga"})

        settings = list_settings()
        # print(settings)

        print(settings.get("template_directory"))
        self.assertTrue(settings.get("template_directory") == "gaga")

    def test_view_settings_in_editor(self):
        view_settings_in_editor()


if __name__ == "__main__":
    run_test_methods(TestSettings.test_view_settings_in_editor)
