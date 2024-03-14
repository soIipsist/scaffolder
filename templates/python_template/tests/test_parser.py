import unittest
import os

from test_base import TestBase, run_test_methods
import time

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parent_directory) 
from utils.sqlite import *
from utils.sqlite_item import SQLiteItem
from utils.date_utils import get_current_date

from constants import *
import subprocess
import sys
from utils.parser import *
import runpy

conn = create_connection('database.db')

command_names = ['view']

test_cmd = command_names[0]
args = None

class TestParser(TestBase):
    def setUp(self) -> None:
        # arguments = ['-d', '24/07']
        arguments = ["args", '-d', '24/07/2023']

        for arg in arguments:
            sys.argv.append(arg)
        
        self.vars = runpy.run_path("parser_test.py", run_name="__main__")
        super().setUp()
    
    def test_arguments(self):
        parser_args = self.vars['parser_args']
        print(parser_args)
        self.assertTrue(len(parser_args)> 0)

    def test_run_command(self):
        parser = self.vars['parser']
        cmd_dict = self.vars['cmd_dict']
        parser:Parser
        parser.run_command(cmd_dict)

    
    def test_run_object_command(self):
        sample  = self.vars['sample']
        parser = self.vars['parser']
        parser:Parser
        cmd_dict = parser.get_object_command_dict(sample)
        parser.run_command(cmd_dict)
    



if __name__ == "__main__": 
    test_methods = [TestParser.test_run_object_command]
    run_test_methods(test_methods)
    