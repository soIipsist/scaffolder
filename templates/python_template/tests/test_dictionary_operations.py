import os

from test_base import TestBase, run_test_methods
import time
from utils.dictionary_operations import *

from utils.sqlite_connection import tables, values, log_table, log_values
from utils.sqlite import *
from utils.dictionary_operations import *

class TestDictionaryUtils(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.nested_dict = {
            'person': {
                "name": "red",
                "surname": "f"
            }
        }
        self.test_dict = {
            "person": 'hi',
            "read": 'write'
        }
        self.test_dict2  = {
            "person": "hi",
            "h": "b"
        }

        self.dict_list = [
            self.test_dict2,
            self.test_dict
        ]

    def test_get_nested_value(self):
        val = get_nested_value(self.nested_dict, ['person', 'surname'])
        self.assertIsNotNone(val)
    
    def test_invert_dict(self):
        inverted = invert_dict(self.test_dict)
        print(inverted)
        self.assertTrue(invert_dict(inverted) == self.test_dict)

    def test_find_dict_list_duplicates(self):
        dups = find_dict_list_duplicates(self.dict_list, 'person')
        self.assertTrue(len(dups) == 2)

    def test_safe_pop(self):
        keys = ['red', 'hello']

        original = self.test_dict
        safe_pop(self.test_dict, keys)
        self.assertTrue(original == self.test_dict)

        keys = ['person']

        safe_pop(self.test_dict, keys)
        self.assertTrue('person' not in self.test_dict.keys())

if __name__ == "__main__":
    methods = [TestDictionaryUtils.test_safe_pop]
    run_test_methods(methods)
