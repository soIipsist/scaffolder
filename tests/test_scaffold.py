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

from utils.func_utils import get_callable_args

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

    def get_destination_dir(self, dest: str):
        destination_dir = os.path.join(self.get_template_directory(), dest)
        Template()

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

    def test_scaffold_repository_no_repo(self):
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

    def test_scaffold_repository(self):
        self.create_repository = True
        self.destination_directory = self.get_destination_dir("android_template")

        args = self.get_scaffold_args()
        args = get_callable_args(scaffold_repository, args)
        self.assertIsNotNone(scaffold_repository(**args))

    def test_create_from_template(self):
        args = self.get_scaffold_args()
        args = get_callable_args(create_from_template, args)
        print(args)

        # add sample template
        d = self.get_template_directory("sample_template")
        template = Template(d)
        template.insert()

        destination_directory = os.path.join(
            self.get_files_directory("scaffold_tests"), "sample_template"
        )
        create_from_template(template.template_directory, destination_directory)


if __name__ == "__main__":
    run_test_methods(TestScaffold.test_scaffold_repository)
