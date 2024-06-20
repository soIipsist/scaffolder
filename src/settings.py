import argparse
from pprint import pp
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.json_utils import overwrite_json_file
from utils.parser import *
from src.constants import *
import subprocess


class SettingsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print(values)
        if len(values) == 1:
            namespace.parameters = values[0]
        else:
            print("Invalid usage")


def list_settings(parameters: list = []):
    if not parameters:
        parameters = scaffolder_metadata.keys()

    settings = {}
    for name in parameters:
        val = scaffolder_metadata.get(name)
        if val is not None:
            print(f"{name}: {val}")
            settings.update({name: val})
    return settings


def update_settings(**args):
    settings = {}

    for key, val in args.items():
        meta_val = scaffolder_metadata.get(key)

        if val != meta_val and val is not None:
            settings.update({key: val})

    new_settings = {**scaffolder_metadata, **settings}
    overwrite_json_file(scaffolder_data_path, new_settings)


def edit_settings(default_editor: str = "vscode"):
    print(f"Default editor set to {default_editor}.")

    if default_editor == "vscode":
        default_editor = "code"
    base_cmd = f"{default_editor} {parent_directory}/src/scaffolder.json"

    subprocess.Popen(base_cmd, shell=True)


def main():

    update_arguments = [
        Argument(name=("-t", "--template_directory")),
        Argument(name=("-d", "--destination_directory")),
        Argument(name=("-n", "--package_name")),
        Argument(name=("-l", "--license")),
        Argument(name=("-a", "--author")),
        Argument(name=("-y", "--year")),
        Argument(name=("-u", "--author")),
        Argument(name=("-v", "--repository_visibility"), type=int, choices=[0, 1, 2]),
        Argument(name=("-s", "--update_template_directory")),
        Argument(name=("-d", "--update_destination_directory")),
        Argument(name=("-f", "--update_files"), nargs="+"),
        BoolArgument(name=("-r", "--create_repository"), default=create_repository),
        BoolArgument(name=("-g", "--gh_check"), default=gh_check),
    ]
    parser_arguments = [Argument(name="parameters", nargs="?", default=None)]

    view_arguments = [
        Argument(name=("-p", "--parameters"), nargs="+"),
    ]

    edit_arguments = [Argument(name=("-e", "--default_editor"), default="vscode")]

    subcommands = [
        SubCommand("update", update_arguments),
        SubCommand("view", view_arguments),
        SubCommand("edit", edit_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)

    cmd_dict = {
        None: list_settings,
        "update": update_settings,
        "view": list_settings,
        "edit": edit_settings,
    }

    parser.run_command(cmd_dict)


if __name__ == "__main__":
    main()
