import os

from test_base import TestBase, run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.sqlite_connection import tables, values, log_table, log_values
from utils.sqlite import *

from tests.test_sqlite_item import log, log2, log3, player, player2, player3, Log, Player


conn = create_connection("database.db")
bad_inputs = [" DROP TABLE tablename;--", "' OR 1=1; --", "id = 1; DROP TABLE Log;", "id = 1; DROP TABLE Player;"]
date_values = ['23/07', '08/04/2024', bad_inputs[1], '05/05', bad_inputs[2]]
bad_filter_condition = bad_inputs[1]

log_items = [log, log2, log3]
player_items = [player, player2, player3]

table_name = 'Player'

class TestSQLite(TestBase):
    def setUp(self) -> None:
        super().setUp()

    def test_create_connection(self):
        self.assertIsNotNone(conn)
    
    def test_sanitize_values(self):
        # sanitize table names
        new_tables = sanitize_values(tables)
        bad_tables = sanitize_values(bad_inputs)
        new_date_values = sanitize_values(date_values)

        print(new_tables)
        print(bad_tables)
        print(new_date_values)

        # self.assertEqual(len(new_tables) == 1)

    
    def test_sanitize_filter_condition(self):
        # test bad filter condition
        
        log.filter_condition = bad_inputs[2]
        filter_condition, params = sanitize_filter_condition(log.filter_condition)

        self.assertIsNotNone(filter_condition)
        self.assertIsNotNone(params)

        # test regular filter condition

        log.filter_condition = "id = 5 AND name = 'red'"
        filter_condition, params = sanitize_filter_condition(log.filter_condition)

        print(filter_condition)
        print(params)


    def test_create_tables(self):
        new_tables = sanitize_values(tables)
        print(new_tables)
        self.assertIsNotNone(new_tables)
        for table, vals in zip(new_tables, values):
            create_table(conn, table, vals)

    def test_get_column_names(self):
        cursor = conn.cursor()
        column_names = get_column_names(cursor, table_name)
        print(column_names)
        self.assertIsNotNone(column_names)

    def test_get_filter_condition(self):
        keys = player.column_names
        filter_condition = get_filter_condition(keys)
        print(filter_condition)
        self.assertIsNotNone(filter_condition)
    
    def test_select_items(self):
        # select all items
        items = select_items(conn, table_name)
        self.assertTrue(isinstance(items, list))
        self.assertTrue(len(items) > 0)
        print(items)

        # select based on filter condition
        player.id = 6
        player.name = 'blue'
        filter_condition = f"id = {player.id} AND name = '{player.name}'"
        items = select_items(conn, table_name, filter_condition, Player)
        for item in items:
            item:Player
            print(item.name)

    def test_insert_items(self):
        id = insert_items(conn, table_name, player_items, ['name', 'total_exp'])
        self.assertIsNotNone(id)
        self.assertTrue(isinstance(id, int))

    def test_update_item(self):
        player.id = 4
        player.total_exp = 9000
        player.name = 'yolo'
        id = update_item(conn, table_name, player.get_unique_object(), player.filter_condition)
        self.assertTrue(id != -1)


    def test_delete_items(self):
        player.id = 4
        print(player.filter_condition)
        id = delete_items(conn, table_name, player.filter_condition)        
        print(id)
        
        # delete all items
        delete_items(conn, table_name, 'all')
        items = select_items(conn, table_name)
        self.assertTrue(len(items) == 0)


    def test_get_random_row(self):

        # test for bad table name
        random_row = get_random_row(conn, bad_inputs[2])
        print(random_row)
        self.assertTrue(len(random_row) == 0)
        # test for valid table name
        random_row = get_random_row(conn, tables[0])
        print(random_row)

        self.assertTrue(len(random_row) > 0)


if __name__ == "__main__":
    test_methods = [TestSQLite.test_get_random_row]
    run_test_methods(test_methods)
