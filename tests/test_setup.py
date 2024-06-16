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
import toml

import configparser


class TestSetup(TestBase):
    def setUp(self) -> None:
        super().setUp()

    def get_dependencies(self):
        requirements_path = f"{parent_directory}/requirements.txt"
        if not os.path.exists(requirements_path):
            os.system("pip freeze > requirements.txt")

        dependencies = read_file(requirements_path).splitlines()

        return dependencies

    def test_create_pyproject_toml(self):
        pyproject_path = f"{parent_directory}/pyproject.toml"
        self.assertTrue(os.path.exists(pyproject_path))

        dependencies = self.get_dependencies()
        pyproject_toml = read_and_parse_file(pyproject_path)
        pyproject_toml["project"]["dependencies"] = dependencies
        dump_data_in_file(pyproject_path, pyproject_toml)

    def test_create_config(self):
        setup_path = f"{parent_directory}/setup.cfg"
        self.assertTrue(os.path.exists(setup_path))

        config_parser = configparser.ConfigParser()
        config_parser.read(setup_path)

        dependencies = "\n".join(self.get_dependencies())
        config_parser.set("options", "install_requires", dependencies)
        print(config_parser.get("options", "install_requires"))

        with open(setup_path, "w") as configfile:
            config_parser.write(configfile)


if __name__ == "__main__":
    run_test_methods(
        [
            TestSetup.test_create_config,
        ]
    )
