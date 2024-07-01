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
from utils.sqlite_connection import db_path, create_db, tables, values

licenses = ["mit", "afl-3.0"]
target_directory = os.getcwd()
author = "soIipsist"


class TestScaffold(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables, values)
        self.template_directory = template_directory
        self.destination_directory = destination_directory
        self.license = license
        self.author = author
        self.year = year
        self.create_repository = create_repository
        self.repository_visibility = repository_visibility
        self.store_template = store_template
        self.repository_name = repository_name

    def get_scaffold_args(self):
        # get scaffold function args
        args = {
            "template_directory": self.template_directory,
            "destination_directory": self.destination_directory,
            "repository_name": self.repository_name,
            "license": self.license,
            "author": self.author,
            "create_repository": self.create_repository,
            "repository_visibility": self.repository_visibility,
            "store_template": self.store_template,
        }

        return args

    def test_scaffold_no_template(self):
        self.template_directory = None
        self.create_repository = False

        args = self.get_scaffold_args()

        with self.assertRaises(ValueError):
            scaffold(**args)

        # no template found test case

        self.template_directory = self.get_template_directory("red")
        args = self.get_scaffold_args()
        with self.assertRaises(ValueError):
            scaffold(**args)

    def test_scaffold(self):
        args = self.get_scaffold_args()
        print(args)
        # scaffold(**args)

    def test_scaffold_repository(self):
        self.create_repository = False

        self.assertIsNone(
            scaffold_repository(
                self.create_repository,
                self.destination_directory,
                self.repository_name,
                self.repository_visibility,
                self.author,
            )
        )

        self.assertIsNotNone(
            scaffold_repository(
                self.create_repository,
                self.destination_directory,
                self.repository_name,
                self.repository_visibility,
                self.author,
            )
        )


if __name__ == "__main__":
    run_test_methods(TestScaffold.test_scaffold_repository)
