from pprint import pp
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from templates.python_template.utils.file_operations import overwrite_json_file
from templates.python_template.utils.parser import *
from src.constants import *
import subprocess
import shutil

def add_template(template_directory:str, template_name:str = None, language:str = 'python', copy_template:bool = True):
    if not isinstance(template_metadata, list):
        raise ValueError("Template metadata not parsed correctly.")
    
    if not template_name:
        template_name = os.path.basename(template_directory)

    if copy_template:

        templates_dir = os.path.join(parent_directory, 'templates', template_name)
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        command = f"cp -r {template_directory}/* {templates_dir}/"
        subprocess.run(command, shell=True)
        template_directory = templates_dir

    template_dict = {"directory": template_directory, "name": template_name, "language": language}
    
    if template_dict not in template_metadata:
        template_metadata.append(template_dict)
        overwrite_json_file(template_data_path,template_metadata)        
    
def delete_template(template:str):
    indices_to_remove = [i for i, t in enumerate(template_metadata) if template == t['name'] or template == t['directory']]
    
    # remove directory entirely
    if len(indices_to_remove) > 0:
        shutil.rmtree(template_metadata[indices_to_remove[0]].get('directory'), ignore_errors=True)

    for index in reversed(indices_to_remove):
        del template_metadata[index]
    
    return indices_to_remove

def list_templates(templates:list = []):

    if not isinstance(template_metadata, list):
        raise ValueError("Template metadata not parsed correctly.")
    
    if not templates:
        templates = template_metadata

    for template in template_metadata:
        if isinstance(template, dict):
            template_directory = template.get('directory')
            template_name = template.get('name', os.path.basename(template_directory))
            template_language = template.get('language')

            print(f"{template_name}: \nDirectory: {template_directory}\nLanguage: {template_language}")

    return templates


if __name__ == "__main__":
    
    add_arguments = [
        DirectoryArgument(name=('-d', '--template_directory')),
        Argument(name=('-n', '--template_name')),
        Argument(name=('-l', '--language'), default='python'),
        Argument(name=('-c', '--copy_template'), type=bool, default=True)
    ]

    delete_arguments = [
        Argument(name=('-t', '--template'))
    ]

    parser_arguments =  [
        Argument(name='templates', nargs='?', default=None)
    ]

    subcommands = [
        SubCommand('add', add_arguments),
        SubCommand('delete', delete_arguments)
    ]

    parser = Parser(parser_arguments, subcommands)

    cmd_dict = {
        None: list_templates,
        "add": add_template,
        "delete": delete_template
    }

    parser.run_command(cmd_dict)

