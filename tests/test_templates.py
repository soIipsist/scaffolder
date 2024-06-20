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


class TestTemplates(TestBase):
    def setUp(self) -> None:
        super().setUp()
        create_db(db_path, tables)
        self.template_directory = self.get_template_directory()
        self.template_name = None
        self.language = "python"
        self.template = Template(
            self.template_directory, self.template_name, self.language
        )

    def get_template_directory(self, template_directory="sample_template"):
        return os.path.join(parent_directory, "templates", template_directory)

    def get_python_template_directory(self):
        path = "/Users/p/Desktop/soIipsis/python_template"
        return path

    def test_get_template_name(self):
        template_directory = self.template.get_template_name()
        print(template_directory)

    def test_add_template(self):
        self.template_directory = self.get_python_template_directory()

        template = add_template(
            self.template_directory,
            self.template_name,
        )
        self.assertIsInstance(template, Template)
        self.assertTrue(len(Template().select_all()) > 0)

    def test_list_templates(self):
        templates = Template().select_all()
        print(templates)

    def test_delete_template(self):
        print(self.template.filter_condition)


if __name__ == "__main__":
    run_test_methods(
        [
            TestTemplates.test_add_template,
        ]
    )
