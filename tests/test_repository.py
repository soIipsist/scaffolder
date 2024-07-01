import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

print(parent_directory)

import requests
from test_base import *
from data.sqlite_data import *
from src.repository import *
from utils.sqlite_connection import create_db


class TestRepository(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.author = "soIipsist"
        self.repository_name = "sample_template"
        self.repository_visibility = 0
        self.git_origin = get_git_origin(self.author, self.repository_name)

    def test_get_repository_visibility(self):
        self.assertTrue(get_repository_visibility("1") == "private")
        self.assertTrue(get_repository_visibility("public") == "public")
        self.assertTrue(get_repository_visibility(0) == "private")
        self.assertTrue(get_repository_visibility(1) == "public")
        self.assertTrue(get_repository_visibility(2) == "internal")
        self.assertTrue(get_repository_visibility("private") == "private")
        self.assertTrue(get_repository_visibility("internal") == "internal")
        self.assertTrue(get_repository_visibility("nothing") == "private")

    def test_is_git_repo(self):

        # print(parent_directory)
        # self.assertTrue(is_git_repo(parent_directory))
        # self.assertFalse(is_git_repo(self.get_template_directory("new_template")))

        self.assertFalse(is_git_repo(os.getcwd()))
        print(os.getcwd())
        self.assertFalse(is_git_repo("/Users/p/Desktop/test"))

    def test_get_repository_name(self):
        print(self.git_origin, self.repository_name)
        self.assertTrue(get_repository_name(self.git_origin) == self.repository_name)

    def test_git_diff(self):
        diff = git_diff()
        self.assertIsNotNone(diff)

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

        git_origin = create_git_repository(
            self.git_origin,
            repository_visibility="public",
            cwd=self.get_template_directory(),
        )

        self.assertIsNotNone(git_origin)

    def test_update_repository(self):
        update_git_repository(
            self.git_origin, self.get_template_directory(), self.repository_visibility
        )

    def test_delete_git_repository(self):
        git_origin = delete_git_repository(self.git_origin)
        self.assertIsNotNone(git_origin)


if __name__ == "__main__":
    run_test_methods(
        [
            TestRepository.test_is_git_repo,
        ]
    )
