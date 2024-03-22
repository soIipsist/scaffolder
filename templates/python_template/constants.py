db_path = "database.db"
player_table = "Player"
player_values = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "total_exp REAL",
    "name TEXT NOT NULL UNIQUE",
]

log_table = "Log"
log_values = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "date_created TEXT NOT NULL",
    "hour_interval INTEGER NOT NULL",
    "hour_tasks TEXT",
    "real_hour_tasks TEXT",
]

tables = [player_table, log_table]
values = [player_values, log_values]
