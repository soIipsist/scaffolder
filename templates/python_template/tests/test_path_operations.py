import os

from test_base import TestBase, run_test_methods

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.path_operations import *


class TestPathUtils(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.test_path = f"{parent_directory}/constants.py"
        self.test_dir = f"{parent_directory}"

    def test_is_valid_dir(self):

        self.assertIsNotNone(is_valid_dir(self.test_dir))

        # test invalid dir
        with self.assertRaises(NotADirectoryError):
            is_valid_dir("")

        self.assertIsNone(is_valid_dir("", False))

    def test_is_valid_path(self):
        self.assertIsNotNone(is_valid_path(self.test_path))

        # test invalid path
        with self.assertRaises(FileNotFoundError):
            is_valid_path("")

        self.assertIsNone(is_valid_path("", False))
        print(self.test_path)


if __name__ == "__main__":
    methods = [TestPathUtils.test_is_valid_dir]
    run_test_methods(methods)
