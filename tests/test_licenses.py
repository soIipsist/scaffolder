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

from data.sqlite_data import *
from src.licenses import *

from utils.sqlite_connection import create_db


class TestLicenses(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.licenses = ["mit", "apache-v2.0"]

    def test_get_license_paths(self):
        # all licenses
        licenses = "all"
        license_paths = get_license_paths(licenses)
        print(license_paths)
        self.assertIsNotNone(license_paths)
        self.assertTrue(len(license_paths) == len(os.listdir(licenses_directory)))

        licenses = ["mit", "afl-3.0", "yolo"]

        license_paths = get_license_paths(licenses)
        print(license_paths)
        self.assertIsNotNone(license_paths)

    def test_view_licenses(self):
        license_paths = view_licenses(self.licenses)
        self.assertIsNotNone(license_paths)

    def test_create_license(self):
        license = "afl-3.0"
        path = create_license(
            license=license,
            destination_directory=destination_directory,
            author=author,
            year=year,
        )
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    run_test_methods(
        [
            TestLicenses.test_view_licenses,
        ]
    )
