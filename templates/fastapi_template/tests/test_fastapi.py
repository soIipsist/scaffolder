import os
import time


parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.sys.path.insert(0, parent_directory)
from python_template.tests.test_base import TestBase, run_test_methods
from fastapi_template.utils import *

class TestFastApi(TestBase):
    def setUp(self) -> None:
        super().setUp()
    
    def test_hash_password(self):
        password = 'hello'
        hashed_password = hash_password(password)

        self.assertIsNotNone(hashed_password)
        self.assertTrue(verify_password(password, hashed_password))
        print(password, hashed_password)
    

if __name__ == "__main__":
    methods = [TestFastApi.test_hash_password]
    run_test_methods(methods)
