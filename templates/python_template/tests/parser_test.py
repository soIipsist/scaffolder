import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parent_directory) 
from utils.sqlite import *
from utils.sqlite_item import SQLiteItem
from utils.date_utils import get_current_date
from utils.parser import *
import sys

arguments = [DateArgument()]
subcommands = [SubCommand('view', arguments), SubCommand('args', arguments)]

def func1():
    print('hi')

def func2():
    print('g')


def func_with_args(date_created):
    print(date_created)

class Sample():
    def __init__(self) -> None:
        pass
    
    def func1(self):
        print('hi')

    def func2(self):
        print('g')

    def args(self, date_created):
        print(date_created)


if __name__  == "__main__":
    parser = Parser()
    parser.add_parser_arguments(arguments)
    parser.create_subcommands(subcommands)

    parser_args = parser.get_command_args()

    cmd_dict = {
        "view": func1,
        "args": func_with_args,
        None: func2
    }

    parser_cmd = parser.get_command_function(cmd_dict)
    print(parser.args)

    sample = Sample()

    # parser_func = parser.get_command_function()
