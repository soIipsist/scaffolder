import json
import os
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.sys.path.insert(0, parent_directory)
from python_template.tests.test_base import TestBase, run_test_methods
from fastapi_template.utils import *
from fastapi.testclient import TestClient

from fastapi_template.main import app

class TestFastApi(TestBase):
    def setUp(self) -> None:
        super().setUp()
        self.client = TestClient(app)
    
    def test_hash_password(self):
        password = 'hello'
        hashed_password = hash_password(password)

        self.assertIsNotNone(hashed_password)
        self.assertTrue(verify_password(password, hashed_password))
        print(password, hashed_password)
    
    def test_routes(self):
        response = self.client.get('/')

        print(response.text)

if __name__ == "__main__":
    methods = [TestFastApi.test_routes]
    run_test_methods(methods)
