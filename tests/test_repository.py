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
from src.repository import *

from utils.sqlite_connection import create_db


class TestRepository(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.author = "soIipsist"
        self.repository_name = "sample_template"

    def test_get_repository_visibility(self):
        self.assertTrue(get_repository_visibility("1") == "private")
        self.assertTrue(get_repository_visibility("public") == "public")
        self.assertTrue(get_repository_visibility(0) == "private")
        self.assertTrue(get_repository_visibility(1) == "public")
        self.assertTrue(get_repository_visibility(2) == "internal")
        self.assertTrue(get_repository_visibility("private") == "private")
        self.assertTrue(get_repository_visibility("internal") == "internal")
        self.assertTrue(get_repository_visibility("nothing") == "private")

    def test_set_repository_visibility(self):
        repo_visibility = set_repository_visibility(
            self.repository_name, get_repository_visibility(1), self.author
        )

        self.assertIsInstance(repo_visibility, str)

    def test_rename_repository(self):
        template_dir = self.get_template_directory()
        os.chdir(template_dir)
        rename_repo(
            os.path.basename("red"), os.path.basename(template_dir), self.author
        )

    def test_create_repository(self):
        template_dir = self.get_template_directory()

        original_dir = os.getcwd()
        os.chdir(template_dir)
        create_git_repository(
            self.repository_name, repository_visibility="public", author="soIipsist"
        )

        os.chdir(original_dir)

    def test_delete_repository(self):
        template_dir = self.get_template_directory()
        delete_git_repository(os.path.basename(template_dir), author="soIipsist")

    def test_git_repo_exists(self):
        print(self.get_template_directory())
        self.assertTrue(git_repo_exists(self.get_template_directory()))

        print(parent_directory)
        self.assertTrue(git_repo_exists(parent_directory))


if __name__ == "__main__":
    run_test_methods(
        [
            TestRepository.test_delete_repository,
            # TestRepository.test_git_repo_exists,
        ]
    )
