import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

print(parent_directory)

import requests
from test_base import *

from data.sqlite_data import *
from utils.sqlite_connection import create_db
from src.languages import *


class TestLanguages(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)

    def test_add_languages(self):
        add_languages()

    def test_detect_language(self):
        # C test
        path = self.get_file("file.c", "c_test_files")
        self.assertTrue(os.path.exists(path))
        lang = detect_language(path)
        self.assertTrue(lang == "c")
        print(lang)

        # C++ test
        path = self.get_file("file.cpp", "cpp_test_files")
        self.assertTrue(os.path.exists(path))
        lang = detect_language(path)
        self.assertTrue(lang == "c++")
        print(lang)

        # python test
        path = self.get_file("file.py", "python_test_files")
        self.assertTrue(os.path.exists(path))
        lang = detect_language(path)
        self.assertTrue(lang == "python")
        print(lang)


if __name__ == "__main__":
    run_test_methods(
        [
            TestLanguages.test_detect_language,
        ]
    )
