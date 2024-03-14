import unittest
import os

from test_base import TestBase, run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parent_directory) 
from utils.sqlite import *
from utils.date_utils import get_current_date
from constants import *
from utils.sqlite_connection import *

db_path = 'database.db'

class TestSQLiteConnection(TestBase):
    def setUp(self) -> None:
        super().setUp()
    
    def test_create_db(self):
        create_db(db_path)

    def test_rebuild_db(self):
        rebuild_db(db_path)

    def test_reset_db(self):
        conn = create_connection(db_path)
        reset_db(conn)
    
    def test_delete_db(self):
        conn = create_connection(db_path)
        delete_db(conn)

if __name__ == "__main__":
    run_test_methods(TestSQLiteConnection.test_create_db)