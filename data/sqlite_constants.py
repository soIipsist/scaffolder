db_path = "scaffolder.db"
template_table = "Template"
template_values = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "template_directory TEXT NOT NULL UNIQUE",
    "name TEXT NOT NULL UNIQUE",
]


tables = [template_table]
values = [template_values]
