from argparse import _SubParsersAction, ArgumentParser
import argparse
from datetime import datetime
from templates.python_template.utils.dictionary_operations import safe_pop

from templates.python_template.utils.path_operations import is_valid_path, is_valid_dir
from templates.python_template.utils.date_utils import get_current_date, parse_date


class Argument:
    name = None
    type = str
    help = ""
    default = None
    choices: list = None
    nargs: int = None
    required: bool = None

    def __init__(
        self,
        name: str = None,
        type=str,
        default=None,
        help="",
        choices=None,
        nargs=None,
        required=None,
        action=None,
    ) -> None:
        self.name = self.get_name(name)
        self.type = type
        self.help = help
        self.default = default
        self.choices = choices
        self.nargs = nargs
        self.required = required
        self.action = action

    def get_name(self, name):
        if name is None:
            return None
        elif isinstance(name, str):
            return (name,)
        elif isinstance(name, tuple):
            return name
        else:
            raise ValueError("Invalid type for the 'name' argument")

    def get_arguments(args: list = []):
        arguments = [
            (
                Argument(**dict(zip(vars(Argument()).keys(), arg)))
                if not isinstance(arg, Argument)
                else arg
            )
            for arg in args
        ]
        return arguments
    
    def get_argument_dictionary(self):

        dictionary = {
            "type": self.type,
            "default": self.default,
            "help": self.help,
            "nargs": self.nargs,
            "action": self.action,
            "required": self.required
        }

        name = self.name[0] if isinstance(self.name, tuple) else self.name
        
        if not(name.startswith('-')):
            safe_pop(dictionary, "required")

        if dictionary.get('action') and not(isinstance(self.action, argparse.Action)):
            safe_pop(dictionary, ["type", "nargs", "default"])

        return dictionary

    def __str__(self) -> str:
        return str(vars(self))

class StoreArgument(Argument):
    def __init__(self, name: str = ("--parameters"), action='store_true') -> None:
        super().__init__(name, action=action)

class DateArgument(Argument):
    def __init__(
        self,
        name: str = ("-d", "--date_created"),
        help="Specify date",
        default=None,
        type=parse_date,
    ) -> None:
        super().__init__(name, help=help, default=default, type=type)


class PathArgument(Argument):
    def __init__(
        self, name: str = ("-p", "--path"), type=is_valid_path, default=None, help=""
    ) -> None:
        super().__init__(name, type, help=help, default=default)


class DirectoryArgument(Argument):
    def __init__(
        self, name: str = "--directory", type=is_valid_dir, default=None, help=""
    ) -> None:
        super().__init__(name, type, help=help, default=default)


class SubCommand:
    subcommand_arguments: list[Argument]
    description: str = ""
    name: str = ""

    def __init__(
        self, name: str, subcommand_arguments: list = [], description=""
    ) -> None:
        self.name = name
        self.subcommand_arguments = Argument.get_arguments(subcommand_arguments)
        self.description = description

        if subcommand_arguments and not all(
            isinstance(argument, Argument) for argument in self.subcommand_arguments
        ):
            raise ValueError("arguments can only be of type Argument.")

    def create_subcommand(self, subparsers):

        # add parser to subparsers
        subcommand = subparsers.add_parser(self.name, description=self.description)
        for arg in self.subcommand_arguments:
            arg: Argument
            arg_dict = arg.get_argument_dictionary()
            # print(arg_dict)
            subcommand.add_argument(
                *arg.name,
                **arg_dict
            )

        return subcommand


class Parser:

    parser_arguments: list[Argument] = []
    subcommands: list[SubCommand] = []

    args = None

    def __init__(self, parser_arguments=[], subcommands=[]) -> None:
        self.parser = ArgumentParser()

        if parser_arguments:
            self.add_parser_arguments(parser_arguments)

        if subcommands:
            self.subparsers = self.parser.add_subparsers(title="Commands", dest="command")
            self.create_subcommands(subcommands)

    def add_parser_arguments(self, parser_arguments: list):

        if not all(
            isinstance(argument, Argument) for argument in self.parser_arguments
        ):
            raise ValueError("arguments can only be of type Argument.")

        self.parser_arguments = Argument.get_arguments(parser_arguments)

        for arg in self.parser_arguments:
            arg: Argument
            arg_dict = arg.get_argument_dictionary()
            # print(arg_dict)
            self.parser.add_argument(
                *arg.name,
                **arg_dict
            )

    def create_subcommands(self, subcommands: list):

        if not all(isinstance(subparser, SubCommand) for subparser in subcommands):
            raise ValueError("subparsers can only be of type Subparser.")

        self.subcommands = subcommands

        for subcommand in self.subcommands:
            subcommand: SubCommand
            subcommand.create_subcommand(self.subparsers)     

    def get_command_function(self, cmd_dictionary: dict, dest: str = "command"):
        """
        Given a dictionary of command-function pairs, return the appropriate function.
        """

        if not self.args:
            raise ValueError('args not defined.')

        if not isinstance(cmd_dictionary, dict):
            raise ValueError("'commands' is not a dictionary.")

        if not isinstance(self.args, dict):
            raise ValueError("'commands' is not a dictionary.")

        main_command = self.args.get(dest)
        func = cmd_dictionary.get(main_command)
        return func

    def get_command_args(self):
        """
        Get parser arguments.
        """
        self.args = vars(self.parser.parse_args())

        cmd = self.args.get("command")
        if cmd:
            subcommand_arguments = next(
                subcommand.subcommand_arguments
                for subcommand in self.subcommands
                if subcommand.name == cmd
            )

            args = {}

            for arg in subcommand_arguments:
                arg: Argument
                arg_name = arg.name
                arg_name = arg_name[1] if len(arg.name) == 2 else arg_name[0]
                arg_name = arg_name.replace("-", "")
                args.update({arg_name: self.args.get(arg_name)})

            return args

        # create parser arguments dictionary
        safe_pop(self.args, "command")

        # remove all arguments that don't matter

        temp_dict = self.args.copy()
        for key, item in self.args.items():
            if not item:
                temp_dict.pop(key)

        return temp_dict


    def get_object_command_dict(self, obj, command_names:list = []): 
        cmd_dict = {}

        object_methods = [method_name for method_name in dir(obj) if callable(getattr(obj, method_name)) and not method_name.startswith('__')]

        if not command_names:
            command_names = object_methods
        
        for name, method in zip(command_names, object_methods):
            cmd_dict.update({name:getattr(obj, method)})

        return cmd_dict
    
    def run_command(self, cmd_dict:dict, dest="command"):
        "Executes a command with parser arguments, requiring a dictionary that links the command name to the associated function to be executed."

        args = self.get_command_args()
        cmd = self.get_command_function(cmd_dict, dest)  

        # add args that have the same name as the function parameters
        from inspect import signature
        call_args = signature(cmd).parameters
        call_args = list(call_args.keys())

        arg_names = list(set(args.keys()).intersection(set(call_args)))

        # print(call_args, arg_names)
        if len(call_args) > len(arg_names) and len(arg_names) !=0:
            raise ValueError(f"Invalid parameters given. Function parameters: {call_args}")
        
        safe_pop(args, 'command')
        cmd(**args)
