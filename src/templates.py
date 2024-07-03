import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.parser import *
from src.constants import *
import shutil

from utils.sqlite_item import *
from data.sqlite_data import *

from src.repository import clone_git_repository


class Template(SQLiteItem):
    template_directory: str
    template_name: str
    language: str
    repository_url: str

    def __init__(
        self,
        template_directory: str = None,
        template_name: str = None,
        language: str = "python",
        repository_url: str = None,
    ) -> None:
        super().__init__(table_values=template_values)
        self.template_directory = template_directory
        self.template_name = self.get_template_name(template_name)
        self.language = language
        self.repository_url = self.get_repository_url(repository_url)
        self.filter_condition = f"template_name = {self.template_name} OR template_directory = {self.template_directory} OR repository_url = {self.repository_url}"

    def get_template_name(self, template_name: str = None):
        if template_name:
            return template_name

        return (
            os.path.basename(self.template_directory)
            if self.template_directory
            else None
        )

    def get_repository_url(self, repository_url: str = None):

        repository_url = (
            repository_url if repository_url is not None else self.template_directory
        )

        if repository_url and repository_url.startswith("https://github.com/"):
            parts = repository_url[len("https://github.com/") :].split("/")

            if len(parts) >= 2 and parts[1]:
                template_name = os.path.basename(repository_url).split(".git")[0]
                self.template_directory = os.path.join(os.getcwd(), template_name)
            return repository_url

    def copy_template(self, destination_directory: str):
        """
        Copies template_directory to specified destination directory.
        """

        if not os.path.exists(self.template_directory):
            raise FileNotFoundError(
                f"Template directory {self.template_directory} does not exist."
            )

        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)

        print(f"Copying template {self.template_directory} to {destination_directory}.")
        shutil.copytree(
            self.template_directory, destination_directory, dirs_exist_ok=True
        )
        return destination_directory

    def remove_template(self):
        shutil.rmtree(self.template_directory, ignore_errors=True)
        print(f"{self.template_name} was deleted successfully.")

    def get_template_description(self):
        return f"Template name: {self.template_name} \nDirectory: {self.template_directory}\nLanguage: {self.language}\n"

    @staticmethod
    def get_template(template: str):
        templ = Template(
            template_directory=template, repository_url=template, template_name=template
        )
        items = templ.select()
        return items[0] if len(items) > 0 else None

    def add_template(
        self,
        destination_directory: str = None,
        store_template: bool = True,
    ):

        destination_directory = (
            os.path.join(os.getcwd(), os.path.basename(self.template_directory))
            if not destination_directory
            else destination_directory
        )

        if self.repository_url:
            clone_git_repository(self.repository_url, cwd=os.getcwd())

        # copy template
        if self.template_directory != destination_directory:
            try:
                self.copy_template(destination_directory)
                print(f"New template directory set to: {destination_directory}.")
            except Exception as e:
                print("Template already exists.")

        self.template_directory = destination_directory

        if store_template:
            i = self.insert()

            if i is None:
                self.update()

        return self

    def delete_template(self, remove_dir: bool = True):
        templ = self.get_template(template=self.template_directory)

        if templ:
            templ.delete()
            if remove_dir:
                templ.remove_template()

    def list_templates(self, templates: list = []):

        for template in templates:
            items = self.get_template(template)

            if len(items) == 1:
                print(items[0])

        if not templates:
            templates = Template().select_all()
            print(templates)
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
        Argument(name=("-s", "--store_template"), type=bool, default=True),
        Argument(name=("-d", "--destination_directory"), default=destination_directory),
    ]

    delete_arguments = [
        Argument(name=("-t", "--template_directory")),
        BoolArgument(name=("-d", "--remove_dir"), default=True),
    ]

    parser_arguments = [Argument(name=("-t", "--template"), default=None)]

    subcommands = [
        SubCommand("add", add_arguments),
        SubCommand("delete", delete_arguments),
    ]

    parser = Parser(parser_arguments, subcommands)
    args = parser.get_command_args()
    template_args = parser.get_callable_args(Template.__init__)

    template = Template(**template_args)

    cmd_dict = {"add": template.add_template, "delete": template.delete_template}
    func = parser.get_command_function(cmd_dict)

    if not func:
        template = Template.get_template(args.get("template"))
        print(template)
    else:
        args = parser.get_callable_args(func)
        func(**args)


if __name__ == "__main__":
    main()
