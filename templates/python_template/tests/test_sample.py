import unittest
import os

from test_base import run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.sqlite import create_connection
from utils.sqlite_connection import *


class TestSample(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_sample(self):
        conn = create_db()
        self.assertIsNotNone(conn)


if __name__ == "__main__":

    run_test_methods(TestSample.test_sample)
