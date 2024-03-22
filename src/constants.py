import os
import pprint

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)
from templates.python_template.utils.file_operations import read_json_file

scaffolder_data_path = f"{parent_directory}/src/scaffolder.json"
scaffolder_metadata = read_json_file(scaffolder_data_path)
scaffolder_metadata:dict

template_data_path = f"{parent_directory}/src/templates.json"
template_metadata = read_json_file(template_data_path)
template_metadata:dict

languages_path = f"{parent_directory}/src/languages.json"
# languages_path2  =  f"{parent_directory}/src/languages2.json"
languages_metadata = read_json_file(languages_path)
languages_metadata:dict

# scaffolder metadata
template_directory = scaffolder_metadata.get('template_directory')
project_directory = scaffolder_metadata.get('project_directory')
update_source_directory = scaffolder_metadata.get('update_source_directory')
update_destination_directory = scaffolder_metadata.get('update_destination_directory')
update_files = scaffolder_metadata.get('update_files')
license = scaffolder_metadata.get('license')
author = scaffolder_metadata.get('author')
git_username = scaffolder_metadata.get('git_username')
create_repository = scaffolder_metadata.get('create_repository')
repository_visibility = scaffolder_metadata.get('repository_visibility')

licenses_directory = f"{parent_directory}/src/licenses"
pp = pprint.PrettyPrinter(indent="3")