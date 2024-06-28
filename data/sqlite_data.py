from pathlib import Path

db_directory = Path(__file__).resolve().parent
db_path = f"{db_directory}/scaffolder.db"

template_table = "Template"
template_values = [
    "template_directory TEXT NOT NULL UNIQUE",
    "template_name TEXT NOT NULL UNIQUE",
    "language TEXT",
    "repository_url TEXT",
]

language_table = "Language"
language_values = [
    "language TEXT NOT NULL UNIQUE",
    "extensions TEXT",
    "function_patterns TEXT",
]

tables = [template_table, language_table]
values = [template_values, language_values]
