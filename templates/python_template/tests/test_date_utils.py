import os

from test_base import TestBase, run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.sqlite import *
from utils.date_utils import *

from tests.test_sqlite_item import log


class TestDateUtils(TestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_get_current_date(self):
        # with valid format
        date_format = "%d/%m"
        date = get_current_date(date_format)
        print(date)
        self.assertIsNotNone(date)

        # with invalid format
        date_format = "hello"
        date = get_current_date(date_format)
        self.assertTrue(date_format == date)

        # with no format
        date = get_current_date()
        print(date)
        self.assertIsNotNone(date)

    def test_get_date_format(self):
        # with no date formats
        log.date_created = "27/02"
        date_format = get_date_format(log.date_created)
        self.assertIsNotNone(date_format)
        print(date_format)

        # with custom date formats (is None)
        date_formats = ["%d/%m"]
        log.date_created = "27/02/2022"
        date_format = get_date_format(log.date_created, date_formats)
        self.assertIsNone(date_format)
        print(date_format)

        # with custom date formats (is not None)
        date_formats = ["%d/%m", "%d/%m/%Y"]
        date_format = get_date_format(log.date_created, date_formats)
        self.assertIsNotNone(date_format)
        print(date_format)

    def test_parse_date(self):
        target_format = "%d/%m"
        date_string = log.date_created

        # date with given format
        date = parse_date(date_string, target_format)
        self.assertIsNotNone(date)
        print(date)

        # date with default format
        date = parse_date(date_string)
        self.assertIsNotNone(date)
        print(date)

    def test_parse_date_2(self):
        target_format = "%d/%m"
        date_string = log.date_created
        date = parse_date(date_string, target_format)
        print(date)

    # Time utils
    def test_get_time_format(self):
        time_string = "11:05:00"
        time_format = get_time_format(time_string)
        print(time_format)
        self.assertIsNotNone(time_format)

        time_string = "he"
        time_format = get_time_format(time_string)
        print(time_format)
        self.assertIsNone(time_format)

        time_string = "11:05"
        time_format = get_time_format(time_string)
        self.assertIsNotNone(time_format)
        print(time_format)

    def test_parse_time(self):
        target_format = "%H:%M"
        time_string = "11:02"
        time = parse_time(time_string, target_format)
        print(time)
        self.assertIsNotNone(time)

        target_format = "red"
        time = parse_time(time_string, target_format)
        self.assertIsNone(time)

    def test_parse_time_range(self):
        time_range = "12:00:03 - 13:00"

        start_time, end_time = parse_time_range(time_range)
        print(start_time)
        print(end_time)
        self.assertIsNotNone(start_time)
        self.assertIsNotNone(end_time)


if __name__ == "__main__":
    date_methods = [TestDateUtils.test_parse_date_2]
    time_methods = [TestDateUtils.test_parse_time_range]
    run_test_methods(date_methods)
