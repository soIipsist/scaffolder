import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from tests.test_base import TestBase, run_test_methods

from src.scaffold import *
from src.settings import *
from src.licenses import *
from src.templates import *
from src.constants import *
from utils.sqlite_connection import db_path, create_db, tables, values
from src.repository import delete_git_repository
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
        self.git_origin = get_git_origin(self.author, self.repository_name)
        self.files = []
        self.function_patterns = []
        self.language = None

    def get_templ_dir(self, dest: str, insert_template=True):
        destination_dir = os.path.join(self.get_template_directory(""), dest)

        if insert_template:
            templ = Template.get_template(destination_dir)
            if templ:
                templ.delete_template()
            templ = Template(destination_dir)
            templ.insert()
        return destination_dir

    def get_dest_dir(self, dest: str):
        return os.path.join(self.get_files_directory("scaffold_tests"), dest)

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
            "files": self.files,
            "function_patterns": self.function_patterns,
            "language": self.language,
        }

        return args

    def test_scaffold_repository(self):
        self.create_repository = False
        # self.create_repository = True
        self.git_origin = "https://github.com/soIipsist/sample_template"
        self.destination_directory = self.get_template_directory()

        # delete_git_repository(self.git_origin, self.destination_directory)
        # return
        # self.assertIsNone(
        #     scaffold_repository(
        #         self.git_origin,
        #         self.create_repository,
        #         self.repository_visibility,
        #         self.destination_directory,
        #     )
        # )
        self.assertIsNotNone(
            scaffold_repository(
                self.git_origin,
                self.create_repository,
                self.repository_visibility,
                self.destination_directory,
            )
        )

    def test_create_from_template(self):
        args = self.get_scaffold_args()
        args = get_callable_args(create_from_template, args)
        print(args)

        destination_directory = self.get_dest_dir("android_template")
        template_directory = self.get_templ_dir("android_template")

        print(template_directory)
        self.assertTrue(os.path.exists(template_directory))
        destination_directory, template_name = create_from_template(
            template_directory, destination_directory
        )
        self.assertTrue(template_name == "android_template")

    def test_scaffold(self):

        args = self.get_scaffold_args()
        scaffold(**args)

    def test_update_destination_files(self):
        self.files = ["sqlite.py", "green", "sqlite_item.py", "bro.py", "parser.py"]
        self.template_directory = "/Users/p/Desktop/soIipsis/python_template"
        self.destination_directory = self.get_template_directory()
        update_destination_files(
            self.files,
            self.template_directory,
            self.destination_directory,
            self.language,
            self.function_patterns,
        )


if __name__ == "__main__":
    run_test_methods(TestScaffold.test_scaffold_repository)
