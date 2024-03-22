import unittest
import os

from test_base import TestBase, run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.sqlite import *
from utils.sqlite_item import SQLiteItem
from utils.date_utils import get_current_date

from constants import *


class Log(SQLiteItem):
    def __init__(
        self,
        id=None,
        date_created: str = None,
        hour_interval=3,
        hour_tasks=None,
        real_hour_tasks=None,
    ) -> None:
        super().__init__(table_values=log_values)
        self.id = id
        self.date_created = date_created if date_created else get_current_date()
        self.hour_interval = hour_interval
        self.hour_tasks = hour_tasks
        self.real_hour_tasks = real_hour_tasks
        self.filter_condition = f"date_created = '{self.date_created}'"

    def get_log_content(self) -> str:
        return self.date_created

    def __str__(self) -> str:
        return self.get_log_content()


class Player(SQLiteItem):
    id = None

    def __init__(self, id=None, total_exp=0, name: str = None) -> None:
        super().__init__(table_values=player_values)
        self.name = name
        self.total_exp = total_exp
        self._id = id
        self._filter_condition = f"id = {self._id}"

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id):
        print()
        self.filter_condition = f"id = {new_id}"
        self._id = new_id

    def get_player_description(self) -> str:
        description = f"""Player: {self.name}\nTotal exp: {self.total_exp}"""
        return description

    def __str__(self) -> str:
        return self.get_player_description()


conn = create_connection("database.db")

log = Log(date_created=get_current_date(), hour_interval=3)
log2 = Log(date_created=get_current_date(), hour_interval=4)
log3 = Log(date_created=get_current_date(), hour_interval=5)

player = Player(name="red", total_exp=100)
player2 = Player(name="green", total_exp=300)
player3 = Player(name="blue", total_exp=20)

bad_inputs = [
    " DROP TABLE tablename;--",
    "' OR 1=1; --",
    "id = 1; DROP TABLE Log;",
    "id = 1; DROP TABLE Player;",
]


class TestSQLiteItem(TestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_insert_item(self):
        player.name = "pro"
        insert_id = player.insert()
        self.assertIsNotNone(insert_id)
        player.name = "red"
        insert_id = player.insert()
        self.assertIsNone(insert_id)

    def test_delete_item(self):
        player.id = 10
        print(player.filter_condition)
        player.delete()

    def test_update_item(self):
        print(player.filter_condition)
        player.update()

    def test_get_item(self):
        player.id = 8
        p = player.get_item()
        p: Player
        print(p.id)
        self.assertIsNotNone(p)

    def test_export_item(self):
        path = os.getcwd() + "/export_test.txt"
        print(player.name)
        player.export_item(path)
        self.assertTrue(os.path.exists(path))

    def test_import_item(self):
        path = os.getcwd() + "/import_test.txt"
        regex = [r"Player: (.+)\n", r"Total exp: (.+)"]
        attr_names = ["name", "total_exp"]

        # dont insert
        player.import_item(path, regex, attr_names, False)
        print(player.name)
        print(player.total_exp)

        # insert
        player.import_item(path, regex, attr_names)


if __name__ == "__main__":
    run_test_methods(TestSQLiteItem.test_import_item)
