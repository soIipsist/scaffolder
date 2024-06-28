import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.parser import *
from src.constants import *
import shutil

from utils.sqlite_item import *
from data.sqlite_data import *


class Template(SQLiteItem):
    template_directory: str
    template_name: str
    language: str
    repository_url: str

    def __init__(
        self,
        template_directory: str = template_directory,
        template_name: str = None,
        language: str = "python",
        repository_url: str = None,
    ) -> None:
        super().__init__(table_values=template_values)
        self.template_directory = template_directory
        self.template_name = self.get_template_name(template_name)
        self.language = language
        self.repository_url = self.get_repository_url(repository_url)
        self.filter_condition = f"template_name = {self.template_name}"

    def get_template_name(self, template_name: str = None):
        if template_name:
            return template_name

        return (
            os.path.basename(self.template_directory)
            if self.template_directory
            else None
        )

    def get_repository_url(self, repository_url: str = None):

        original_dir = self.template_directory

        if self.template_directory and self.template_directory.startswith(
            "https://github.com/"
        ):
            repository_url = self.template_directory
            original_dir = None

        parts = repository_url[len("https://github.com/") :].split("/")

        if len(parts) >= 2 and parts[1]:
            template_name = parts[1]
            self.template_directory = (
                os.path.join(os.getcwd(), template_name)
                if original_dir is None
                else original_dir
            )

        return repository_url

    def copy_template(self, template_directory: str, destination_directory=None):
        """
        Copies template_directory to specified destination directory.
        """

        if not os.path.exists(template_directory):
            raise FileNotFoundError(
                f"Template directory {template_directory} does not exist."
            )

        destination_directory = (
            os.path.join(parent_directory, "templates", self.template_name)
            if destination_directory is None
            else destination_directory
        )

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        print(f"Copying template {template_directory} to {destination_directory}.")
        shutil.copytree(template_directory, destination_directory, dirs_exist_ok=True)
        return destination_directory

    def remove_template(self):
        shutil.rmtree(self.template_directory, ignore_errors=True)
        print(f"{self.template_directory} was deleted successfully!")

    def get_template_description(self):
        return f"Template name: {self.template_name} \nDirectory: {self.template_directory}\nLanguage: {self.language}\n"

    @staticmethod
    def get_template(template_path_or_name: str):

        try:
            if is_valid_dir(template_path_or_name, False):
                templ = Template(template_directory=template_path_or_name)

            else:
                templ = Template(template_name=template_path_or_name)
                items = templ.select()
                return items[0] if len(items) > 0 else None

            return templ
        except Exception as e:
            print("Exception: ", e)

    def add_template(
        self,
        copy_template: bool = True,
    ):
        from repository import clone_repository

        if self.repository_url:
            clone_repository(self.template_directory, cwd=self.template_directory)
            print(f"New cloned directory set to: {template_directory}.")
            copy_template = False

        if copy_template:
            template_dir = self.copy_template(self.template_directory)
            self.template_directory = template_dir
        self.insert()

        print("Template directory: ", self.template_directory)
        return self

    def delete_template(self, remove_dir: bool = True):
        templ = self.get_template(template_path_or_name=self.template_directory)

        if templ:
            templ.delete()
            if remove_dir:
                templ.remove_template()

    def list_templates(templates: list = []):

        for template in templates:
            temp = Template(template_directory=template, template_name=template)

            items = temp.select(
                f"template_directory = {temp.template_directory} OR template_name = {temp.template_name}"
            )

            if len(items) == 1:
                print(items[0])
        if not templates:
            print(Template().select_all())
        return templates

    def __str__(self) -> str:
        return self.get_template_description()

    def __repr__(self) -> str:
        return self.get_template_description()


def main():
    add_arguments = [
        Argument(name=("-t", "--template_directory"), default=template_directory),
        Argument(name=("-n", "--template_name"), default=repository_name),
        Argument(name=("-l", "--language"), default="python"),
        Argument(name=("-c", "--copy_template"), type=bool, default=True),
    ]

    delete_arguments = [
        Argument(name=("-t", "--template_directory")),
        BoolArgument(name=("-d", "--remove_dir"), default=True),
    ]

    parser_arguments = [
        Argument(name=("-t", "--template_names"), nargs="+", default=[])
    ]

    subcommands = [
        SubCommand("add", add_arguments),
        SubCommand("delete", delete_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)
    args = parser.get_command_args()
    template_args = parser.get_callable_args(Template.__init__)

    template = Template(**template_args)

    temp = template.select()

    if len(temp) > 0:
        template = temp[0]
    else:
        pass

    cmd_dict = {"add": template.add_template, "delete": template.delete_template}
    func = parser.get_command_function(cmd_dict)

    # if not func:
    #     template_names = args.get("template_names")
    #     for t in template_names:
    #         t = Template(template_name=t).select()
    #         if t:
    #             print(t)
    # else:
    #     args = parser.get_callable_args(func)
    #     func(**args)


if __name__ == "__main__":
    main()
