import datetime
import os
import pprint


parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from src.repository import get_author
from src.languages import Language
from utils.json_utils import read_json_file

scaffolder_data_path = f"{parent_directory}/data/scaffolder.json"
scaffolder_metadata = read_json_file(scaffolder_data_path)
scaffolder_metadata: dict

languages = Language().select_all()

# scaffolder metadata
template_directory = scaffolder_metadata.get("template_directory")
destination_directory = scaffolder_metadata.get(
    "destination_directory",
    os.path.join(os.getcwd(), os.path.basename(template_directory)),
)
repository_name = scaffolder_metadata.get(
    "repository_name", os.path.basename(destination_directory)
)

# update vars
files = scaffolder_metadata.get("files", [])
language = scaffolder_metadata.get("language", None)
function_patterns = scaffolder_metadata.get("function_patterns", [])

license = scaffolder_metadata.get("license", "mit")
year = scaffolder_metadata.get("year", str(datetime.datetime.now().year))
author = scaffolder_metadata.get("author", get_author())
create_repository = scaffolder_metadata.get("create_repository", 0)
clone_repository = scaffolder_metadata.get("clone_repository", 0)
store_template = scaffolder_metadata.get("store_template", 1)
repository_visibility = scaffolder_metadata.get("repository_visibility", 0)
gh_check = scaffolder_metadata.get("gh_check")
licenses_directory = f"{parent_directory}/data/licenses"
pp = pprint.PrettyPrinter(indent="3")
