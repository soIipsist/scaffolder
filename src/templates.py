from pprint import pp
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from utils.json_utils import overwrite_json_file
from utils.parser import *
from src.constants import *
import subprocess
import shutil

from utils.sqlite_item import *
from data.sqlite_data import *


class Template(SQLiteItem):
    template_directory: str
    language: str
    template_name: str

    def __init__(
        self, template_directory: str, template_name: str, language: str = "python"
    ) -> None:
        super().__init__(table_values=template_values)
        self.template_directory = template_directory
        self.template_name = template_name
        self.language = language

    def get_template_directory(self, template_directory: str):

        # check if the directory is valid
        if is_valid_dir(template_directory, False):
            return template_directory


def get_template_directory(template: str):

    if is_valid_dir(template, False):
        template_directory = template
    else:
        raise ValueError(
            f"Template {template} does not exist. To add a new template, use the `templates add` command."
        )

    if not os.path.exists(template_directory):
        raise ValueError(f"template directory {template_directory} does not exist.")

    return template_directory


def add_template(
    template_directory: str,
    template_name: str = None,
    language: str = "python",
    copy_template: bool = True,
):

    template_name = (
        os.path.basename(template_directory) if not template_name else template_name
    )
    template_directory = get_template_directory(template_directory)

    if copy_template:

        templates_dir = os.path.join(parent_directory, "templates", template_name)
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)

        command = f"cp -r {template_directory}/* {templates_dir}/"
        subprocess.run(command, shell=True)
        template_directory = templates_dir


def delete_template(template: str):

    # remove directory entirely
    if len(template_indices) > 0:
        shutil.rmtree(
            template_metadata[template_indices[0]].get("directory"), ignore_errors=True
        )

    return template_indices


def list_templates(templates: list = []):

    if not isinstance(template_metadata, list):
        raise ValueError("Template metadata not parsed correctly.")

    if not templates:
        templates = template_metadata

    for template in template_metadata:
        if isinstance(template, dict):
            template_directory = template.get("directory")
            template_name = template.get("name", os.path.basename(template_directory))
            template_language = template.get("language")

            template_directory = template_directory.replace(
                "__PARENTDIR__", parent_directory
            )

            print(
                f"Template name: {template_name} \nDirectory: {template_directory}\nLanguage: {template_language}\n"
            )

    return templates


if __name__ == "__main__":

    add_arguments = [
        DirectoryArgument(name=("-t", "--template_directory")),
        Argument(name=("-n", "--template_name")),
        Argument(name=("-l", "--language"), default="python"),
        Argument(name=("-c", "--copy_template"), type=bool, default=True),
    ]

    delete_arguments = [Argument(name=("-t", "--template"))]

    parser_arguments = [Argument(name="templates", nargs="?", default=None)]

    subcommands = [
        SubCommand("add", add_arguments),
        SubCommand("delete", delete_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)

    cmd_dict = {None: list_templates, "add": add_template, "delete": delete_template}

    parser.run_command(cmd_dict)
