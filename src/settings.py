import argparse
from pprint import pp
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from templates.python_template.utils.file_operations import overwrite_json_file
from templates.python_template.utils.parser import *
from src.constants import *

class SettingsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(values)
        if len(values) == 1:
            namespace.parameters = values[0]            
        else:
            print("Invalid usage")


def list_settings(parameters:list = []):
    if not parameters:
        parameters = scaffolder_metadata.keys()

    settings = {}
    for name in parameters:
        val = scaffolder_metadata.get(name)
        if val is not None:
            print(f"{name}: {val}")
            settings.update({name : val})
    return settings

def update_settings(**args):
    settings = {}

    for key, val in args.items():
        if val is not None:
            settings.update({key: val})
    
    new_settings = {**scaffolder_metadata, **settings}
    overwrite_json_file(scaffolder_data_path, new_settings)


if __name__ == "__main__":
    
    update_arguments = [
        DirectoryArgument(name=('-t', '--template_directory')),
        DirectoryArgument(name=('-p', '--project_directory')),
        Argument(name=('-l', '--license')),
        Argument(name=('-a', '--author')),
        Argument(name=('-u', '--git_username')),
        Argument(name=('-v', '--repository_visibility'), type=int),
        Argument(name=('-s', '--update_source_directory')),
        Argument(name=('-d', '--update_destination_directory')),
        Argument(name=('-f', '--update_files'), nargs='?'),
        Argument(name=('-r', '--create_repository'), type=bool, default=False),
        Argument(name=('-g', '--gh_check'), type=bool, default=False),
    ]
    parser_arguments =  [
        Argument(name='parameters', nargs='?', default=None)
    ]

    view_arguments = [
        Argument(name=('-p', '--parameters'), nargs='+'),
    ]

    subcommands = [
        SubCommand('update', update_arguments),
        SubCommand('view', view_arguments)
    ]

    parser = Parser(parser_arguments, subcommands)

    cmd_dict = {
        None: list_settings,
        "update": update_settings,
        "view": list_settings
    }

    parser.run_command(cmd_dict)

