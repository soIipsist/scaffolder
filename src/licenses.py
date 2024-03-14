import subprocess
import os
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from templates.python_template.utils.file_operations import read_file, overwrite_file
from templates.python_template.utils.path_operations import is_valid_path
from src.constants import *
from templates.python_template.utils.parser import *
import re
# from datetime import 

def get_licenses(licenses:list = []):
    if not isinstance(licenses, list):
        licenses = [licenses]

    license_paths = os.listdir(licenses_directory)
    license_names = [os.path.basename(path) for path in license_paths]
    
    if not licenses or licenses == 'all':
        licenses = license_names

    license_paths = [is_valid_path(os.path.join(licenses_directory, license), False) for license in licenses]
    return license_paths

def create_license(license:str, target_directory:str, author:str, year:str = datetime.now().year):
    
    license_path = get_licenses(license)[0]

    if license_path:
        command = f"cp {license_path} {target_directory}"
        subprocess.run(command, shell=True)
        
        # replace where author and year are in license
        new_path = os.path.join(target_directory, license)
        content = read_file(new_path)

        new_content  = re.sub(r'\{author\}', author, content)
        new_content = re.sub(r'\{year\}', str(year), new_content)
        overwrite_file(new_path,new_content)

        return new_path

def view_license(licenses: list = []):

    if not isinstance(licenses, list):
        licenses = [licenses]
    
    license_paths = get_licenses(licenses)
    
    for path in license_paths:
        content = read_file(path, 'utf-8')
        print(content)
        
    return license_paths


if __name__ == "__main__":
    parser_arguments = [
        Argument(name=('-l', '--licenses'), nargs='+')
    ]

    parser = Parser(parser_arguments)
    args = parser.get_command_args()
    view_license(**args)
