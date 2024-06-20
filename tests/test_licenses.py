import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

print(parent_directory)

import requests
from test_base import *

from utils.file_utils import (
    read_file,
    read_and_parse_file,
    dump_data_in_file,
    overwrite_file,
)

from src.templates import *

from utils.sqlite_connection import create_db


class TestLicenses(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)

    def test_get_licenses(self):
        pass


if __name__ == "__main__":
    run_test_methods(
        [
            TestLicenses.test_list_templates,
        ]
    )
