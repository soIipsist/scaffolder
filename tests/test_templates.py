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
        print(self.get_template_directory())
        self.template = Template(template_directory=self.get_template_directory())

    def get_template_directory(self, template_directory="sample_template"):
        return os.path.join(parent_directory, "templates", template_directory)

    def test_add_template(self):
        add_template()

    def test_list_templates(self):
        templates = Template().select_all()
        print(templates)

    def test_delete_template(self):
        print(db_path)


if __name__ == "__main__":
    run_test_methods(
        [
            TestTemplates.test_delete_template,
        ]
    )
