import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from tests.test_base import TestBase, run_test_methods

from src.scaffold import *
from src.settings import *
from src.licenses import *
from src.templates import *
from src.constants import *
from data.sqlite_data import db_path
from utils.sqlite_connection import create_db, tables, values
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
        self.repository_name = None
        self.git_origin = get_git_origin(self.author, self.repository_name)
        self.files = []
        self.function_patterns = function_patterns
        self.function_names = function_names
        self.language = language
        self.replace_name = replace_name

    def get_templ_dir(self, dest: str, insert_template=True):
        destination_dir = os.path.join(self.get_template_directory(""), dest)

        if insert_template:
            templ = Template.get_template(destination_dir)
            if templ:
                templ.delete_template()
            templ = Template(destination_dir)
            templ.insert()
        return destination_dir

    def get_destination_directory(self, dest: str = "sample_template"):
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
            "function_names": self.function_names,
            "language": self.language,
            "replace_name": self.replace_name,
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

    def test_scaffold(self):
        # Template().delete("all")
        # templ = Template(self.get_template_directory())
        # templ = Template(self.git_origin)
        # print(templ.template_directory, templ.repository_url, templ.template_name)
        # 1) new template without creating repo
        # 2) new template without creating repo with files
        # 3) new template without creating repo with files and function names
        # 4) new template creating repo
        # 5) new template creating repo with files
        # 6) new template creating repo with files and function names

        self.create_repository = False
        self.template_directory = self.get_template_directory()
        self.destination_directory = self.get_destination_directory("sample_template_2")
        # self.repository_name = None

        self.files = []
        self.function_names = []
        self.license = "mit-0"
        self.store_template = True
        self.create_repository = True

        args = self.get_scaffold_args()
        scaffold(**args)

    def test_update_destination_files(self):
        # files are defined
        self.files = ["hello.py", "update.py"]
        # files are not defined
        # self.files = []

        # template_directory of a predefined template
        self.template_directory = self.get_template_directory()
        self.destination_directory = self.get_destination_directory()
        self.function_names = ["hello2"]

        args = get_callable_args(update_destination_files, self.get_scaffold_args())
        print(args)

        if not self.files:
            self.assertIsNone(update_destination_files(**args))
        else:
            self.assertIsNotNone(update_destination_files(**args))


if __name__ == "__main__":
    run_test_methods(TestScaffold.test_scaffold)
