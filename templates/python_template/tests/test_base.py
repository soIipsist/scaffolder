import unittest
import os
import subprocess
import inspect

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)

# from templates.python_template.utils.sqlite import create_connection, close_connection, create_table, delete_items
from pprint import PrettyPrinter

from utils.sqlite_connection import reset_db, delete_db, create_db


class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.logging = True
        self.extension = "json"
        self.pp = PrettyPrinter(indent=3)

    def execute_cmd(self, cmd):
        os.chdir(f"{parentdir}/src")
        print(cmd)
        completed_process = subprocess.run(cmd, shell=True)
        exit_code = completed_process.returncode
        self.assertEqual(exit_code, 0)

    def log_data(self, *args, **kwargs):
        if self.logging:
            for d in args:
                print(d)

    @classmethod
    def generate_default_test_methods(self):
        methods = [
            method_name.replace("test_", "")
            for method_name in dir(self)
            if callable(getattr(self, method_name)) and method_name.startswith("test")
        ]
        return methods


def run_tests(test_methods: list, index: int = None):
    test_case = None
    if index is not None:
        test_case = test_methods[index]
        print(f"Running test '{test_case}'...")
    unittest.main(defaultTest=test_case)


def run_test_methods(test_methods: list):

    if callable(test_methods):
        test_methods = [test_methods]

    default_tests = []
    for test_method in test_methods:
        name = test_method.__name__
        class_name = test_method.__qualname__.split(".")[0]

        default_test = f"{class_name}.{name}"
        default_tests.append(default_test)

    unittest.main(defaultTest=default_tests)


if __name__ == "__main__":
    unittest.main()
