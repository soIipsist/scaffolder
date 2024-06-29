import os

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname((os.path.abspath(__file__))))
)
os.sys.path.insert(0, parent_directory)

import requests
from test_base import *


from src.templates import *

from utils.sqlite_connection import create_db

from utils.sqlite import bad_inputs


class TestTemplates(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.template_directory = self.get_template_directory()
        self.template_name = None
        self.language = "python"
        # self.repository_url = None
        self.repository_url = "https://github.com/soIipsist/adb-wrapper"

    def get_template_args(self):
        return {
            "template_directory": self.template_directory,
            "template_name": self.template_name,
            "language": self.language,
            "repository_url": self.repository_url,
        }

    def test_get_repository_url(self):

        self.repository_url = "https://github.com/soIipsist/adb-wrapper"
        template_args = self.get_template_args()
        template = Template(**template_args)

        self.assertTrue(template.repository_url == self.repository_url)
        self.assertTrue(
            template.template_directory == os.path.join(os.getcwd(), "adb-wrapper")
        )
        print(template.template_directory)
        print(template.repository_url)

        # test with both template_dir and repo_url
        self.template_directory = self.get_template_directory()

        template_args = self.get_template_args()
        print(template_args)
        template = Template(**template_args)

        self.assertTrue(template.repository_url == self.repository_url)
        self.assertTrue(
            template.template_directory == os.path.join(os.getcwd(), "adb-wrapper")
        )

    def test_get_repository_url_with_dir(self):
        self.repository_url = None
        self.template_directory = None
        template_args = self.get_template_args()
        template = Template(**template_args)

        self.assertTrue(template.template_directory == None)
        self.assertTrue(template.repository_url == None)

        self.template_directory = self.get_template_directory()
        template_args = self.get_template_args()
        template = Template(**template_args)

        self.assertTrue(template.template_directory == self.get_template_directory())
        self.assertTrue(template.repository_url == None)

    def test_get_template_name(self):
        template = Template(self.get_template_directory())
        template_name = template.get_template_name()
        self.assertTrue(os.path.basename(template.template_directory) == template_name)
        print(template_name)

    def test_add_template(self):
        self.template_directory = self.get_template_directory()
        template_args = self.get_template_args()

        print(template_args)
        # return
        template = Template(**template_args)

        print(template.get_unique_object())
        return
        template = template.add_template(copy_template=True)
        self.assertIsInstance(template, Template)
        self.assertTrue(len(Template().select_all()) > 0)

    def test_list_templates(self):
        templates = Template().list_templates()
        self.assertTrue(len(templates) > 0)

    def test_delete_template(self):
        template = Template(self.get_template_directory())
        print(template.filter_condition)

    def test_get_template(self):
        template = None
        temp = Template.get_template(template)
        self.assertTrue(temp == None)

        # get by name
        template = "chess_bot"
        temp = Template.get_template(template)
        print(temp)
        self.assertTrue(isinstance(temp, Template))
        self.assertTrue(temp is not None)

        # get by dir
        template = "/Users/p/Desktop/soIipsis/scaffolder/src/chess_bot"
        temp = Template.get_template(template)
        print(temp)
        self.assertTrue(isinstance(temp, Template))
        self.assertTrue(temp is not None)

        # get by repo url
        template = "https://github.com/soIipsist/chess_bot"
        temp = Template.get_template(template)
        print(temp)
        self.assertTrue(isinstance(temp, Template))
        self.assertTrue(temp is not None)
        # bad input
        template = "/Users/p/Desktop/soIipsis/scaffolder"
        temp = Template.get_template(template)
        self.assertTrue(temp == None)


if __name__ == "__main__":
    run_test_methods(
        [
            TestTemplates.test_get_template,
        ]
    )
