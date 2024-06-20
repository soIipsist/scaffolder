import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.parser import *
from src.constants import *
import subprocess
import shutil

from utils.sqlite_item import *
from data.sqlite_data import *


class Template(SQLiteItem):
    template_directory: str
    template_name: str
    language: str

    def __init__(
        self,
        template_directory: str = None,
        template_name: str = None,
        language: str = "python",
    ) -> None:
        super().__init__(table_values=template_values)
        self.template_directory = template_directory
        self.template_name = self.get_template_name(template_name)
        self.language = language
        self.filter_condition = f"template_name = {self.template_name}"

    def get_template_name(self, template_name: str = None):
        if template_name:
            return template_name

        return (
            os.path.basename(self.template_directory)
            if self.template_directory
            else None
        )

    def copy_template(self):
        """
        Copies template_directory to 'templates' if called
        """

        templates_dir = os.path.join(parent_directory, "templates", self.template_name)

        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)

        command = f"cp -r {template_directory}/* {templates_dir}/"
        subprocess.run(command, shell=True)
        template_directory = templates_dir

    def remove_template(self):
        shutil.rmtree(self.template_directory, ignore_errors=True)

    def __str__(self) -> str:
        return f"Template name: {self.template_name} \nDirectory: {self.template_directory}\nLanguage: {self.language}\n"


def get_template(template_path_or_name: str):
    if is_valid_dir(template_path_or_name):
        templ = Template(template_directory=template_path_or_name)
    else:
        templ = Template(template_name=template_path_or_name)
        items = templ.select()
        return items[0] if len(items) > 0 else None
    return templ


def add_template(
    template_directory: str,
    template_name: str = None,
    language: str = "python",
    copy_template: bool = True,
):
    template = Template(template_directory, template_name, language)
    template.insert()

    if copy_template:
        template.copy_template()

    return template


def delete_template(template: str, remove_dir=True, delete_repo=False):
    template = get_template(template_path_or_name=template)
    template: SQLiteItem
    template.delete()
    # remove directory entirely
    if remove_dir:
        template.remove_template()

    if delete_repo:
        template.delete()


def list_templates(templates: list = None):
    for template in templates:
        temp = Template(
            template_directory=template,
        )

        items = temp.select()

        if len(items) == 1:
            print(items[0])

    return templates


def main():
    add_arguments = [
        DirectoryArgument(name=("-t", "--template_directory")),
        Argument(name=("-n", "--template_name")),
        Argument(name=("-l", "--language"), default="python"),
        Argument(name=("-c", "--copy_template"), type=bool, default=True),
    ]

    delete_arguments = [
        Argument(name=("-t", "--template")),
        BoolArgument(name=("-d", "--remove_dir"), default=True),
        BoolArgument(name=("-r", "--remove_repo"), default=False),
    ]

    parser_arguments = [Argument(name="templates", nargs="?", default=None)]

    subcommands = [
        SubCommand("add", add_arguments),
        SubCommand("delete", delete_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)
    cmd_dict = {None: list_templates, "add": add_template, "delete": delete_template}
    parser.run_command(cmd_dict)


if __name__ == "__main__":
    main()
