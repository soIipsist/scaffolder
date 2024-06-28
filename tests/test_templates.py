import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

print(parent_directory)

import requests
from test_base import *


from src.templates import *

from utils.sqlite_connection import create_db


class TestTemplates(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.template_directory = self.get_template_directory()
        self.template_name = None
        self.language = "python"
        # self.repository_url = None
        self.repository_url = "https://github.com/soIipsist/adb-wrapper"
        self.template = Template(
            self.template_directory,
            self.template_name,
            self.language,
            self.repository_url,
        )

    def get_template_args(self):
        return {
            "template_directory": self.template_directory,
            "template_name": self.template_name,
            "language": self.language,
            "repository_url": self.repository_url,
        }

    def test_get_repository_url(self):

        url = "https://github.com/soIipsist/adb-wrapper"
        self.repository_url = self.template.get_repository_url(url)
        template_args = self.get_template_args()
        self.template = Template(**template_args)
        self.assertTrue(self.template.repository_url == self.repository_url)
        self.assertTrue(
            self.template.template_directory == os.path.join(os.getcwd(), "adb-wrapper")
        )

    def test_get_template_name(self):
        template_directory = self.template.get_template_name()
        print(template_directory)

    def test_add_template(self):
        self.template_directory = self.get_template_directory()
        template_args = self.get_template_args()

        print(template_args)
        # return
        template = Template(**template_args)

        print(template.get_unique_object())
        return
        template = self.template.add_template(copy_template=True)
        self.assertIsInstance(template, Template)
        self.assertTrue(len(Template().select_all()) > 0)

    def test_list_templates(self):
        templates = Template().list_templates()
        self.assertTrue(len(templates) > 0)

    def test_delete_template(self):
        print(self.template.filter_condition)


if __name__ == "__main__":
    run_test_methods(
        [
            TestTemplates.test_get_repository_url,
        ]
    )
