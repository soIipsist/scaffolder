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

    def test_add_languages():
        add_languages()

    def test_detect_language():
        pass


if __name__ == "__main__":
    run_test_methods(
        [
            TestLanguages.test_add_languages,
        ]
    )
