import os

from pydantic import BaseModel

parent_directory = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
os.sys.path.insert(0, parent_directory)
from python_template.tests.test_base import TestBase, run_test_methods
from fastapi_template.utils import *
from fastapi.testclient import TestClient

from fastapi_template.main import app
from fastapi_template.schemas.user import UserIn, UserUpdate
from fastapi_template.schemas.post import PostSchema
from fastapi_template.database import run_postgres_script


sample_user = UserIn(name="blue", surname="red", username="red", password="red")
sample_updated_user = UserUpdate(
    id=3, name="yo", surname="world", username="red", password="red"
)
sample_post = PostSchema(title="post", content="content", owner_id=1)


class TestFastApi(TestBase):
    def setUp(self) -> None:
        super().setUp()
        # reset db

        # query_path = os.path.join(parent_directory, 'fastapi_template','queries', 'delete_tables.sql')
        # run_postgres_script(query_path)
        import warnings

        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self.client = TestClient(app)

    def test_hash_password(self):
        password = "hello"
        hashed_password = hash_password(password)

        self.assertIsNotNone(hashed_password)
        self.assertTrue(verify_password(password, hashed_password))
        print(password, hashed_password)

    def create_route(self, route_name: str, obj: BaseModel):
        response = self.client.post(route_name, json={**obj.model_dump()})
        return response

    def test_create_user(self):
        response = self.create_route("/users", sample_user)
        self.assertIsNotNone(response)
        print(response.status_code)
        print(response.json())

    def test_create_post(self):
        response = self.create_route("/posts", sample_post)
        self.assertIsNotNone(response)
        print(response.status_code)
        print(response.json())

    def test_list_all(self):
        response = self.client.get("/users")
        print(response.json())
        self.assertTrue(isinstance(response.json(), list))

    def test_update_user(self):
        sample_user.name = "hello"
        response = self.client.put(
            f"/users/{sample_updated_user.id}",
            json={**sample_updated_user.model_dump()},
        )
        print(response.status_code)

    def test_delete_user(self):
        response = self.client.delete(f"/users/{sample_updated_user.id}")
        self.assertIsNotNone(response)
        print(response.status_code)


if __name__ == "__main__":
    methods = [TestFastApi.test_create_user, TestFastApi.test_create_post]
    methods2 = [TestFastApi.test_list_all]
    run_test_methods(methods2)
