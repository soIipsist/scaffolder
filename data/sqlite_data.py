from pathlib import Path

parent_directory = Path(__file__).resolve().parent
db_path = f"{parent_directory}/scaffolder.db"

template_table = "Template"
template_values = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "template_directory TEXT NOT NULL UNIQUE",
    "template_name TEXT NOT NULL UNIQUE",
    "language TEXT",
]


tables = [template_table]
values = [template_values]
