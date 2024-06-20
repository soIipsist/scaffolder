import sqlite3
from ast import literal_eval
import re

bad_inputs = [
    "1; DROP TABLE Player; --",
    " DROP TABLE Player;--",
    "' OR 1=1; --",
    "id = 1; DROP TABLE Log;",
    "id = 1; DROP TABLE Player;",
    "id = '1' OR '1'='1'",
    "id = '1' UNION SELECT * FROM Player",
]


def create_connection(database_path: str):
    """
    Create a connection to an SQLite database.
    """
    try:
        conn = sqlite3.connect(database_path)
        return conn
    except sqlite3.Error as e:
        print("Error connecting to the database:", e)
        print("Database path: ", database_path)
        return None


def sanitize_values(values: list):
    """
    Sanitize values by removing non-word characters.
    """
    expression = r"\W+"

    from utils.date_utils import get_date_format
    from utils.url_utils import is_url
    from utils.path_utils import is_valid_path

    if not isinstance(values, list):
        values = [values]

    for i, value in enumerate(values):
        if (
            not get_date_format(value)
            and not is_url(value, False)
            and not is_valid_path(value, False)
        ):
            values[i] = re.sub(expression, "", value)
    return values


def get_filter_condition(filter_condition: str, default_params: list = None):
    """
    Sanitizes filter condition of type id = '1'. Returns the filter condition with placeholders included and
    a tuple of sanitized parameters.
    """

    if not isinstance(filter_condition, str):
        raise ValueError("filter_condition must be of type str.")

    filter_condition_keys = []
    sanitized_params = []
    keywords = []

    pattern = r"(\s+AND\s+|\s+OR\s+|\s+NOT\s+)"
    parts = re.split(pattern, filter_condition)

    comparison_operators = [
        "!=",
        "<>",
        ">=",
        "<=",
        ">",
        "<",
        "=",
    ]

    # Check for SQL injection patterns
    sql_injection_patterns = [
        r"(\bOR\b\s+\d+\s*=\s*\d+)",
        r"(\bOR\b\s*true\b)",
        r"(\bAND\b\s*false\b)",
        r"(\bOR\b\s*1\s*=\s*1)",
        r"(--|;|\/\*|\*\/|\bEXEC\b|\bUNION\b|\bSELECT\b|\bINSERT\b|\bUPDATE\b|\bDELETE\b)",
        r"(\bOR\b\s*'[^']+'\s*=\s*'[^']+')",
    ]

    for pattern in sql_injection_patterns:
        if re.search(pattern, filter_condition, re.IGNORECASE):
            raise ValueError("Potential SQL injection detected.")

    # Process the split parts
    conditions = []
    for part in parts:
        part = part.strip()
        if part in ("AND", "OR", "NOT"):
            keywords.append(part)
        else:
            for operator in comparison_operators:
                if operator in part:

                    key, value = re.split(
                        r"\s*" + re.escape(operator) + r"\s*", part, 1
                    )
                    key = key.strip()
                    value = value.strip().strip(
                        "'"
                    )  # Assuming values are enclosed in single quotes
                    filter_condition_keys.append(key)
                    sanitized_params.append(value)
                    conditions.append(f"{key} {operator} ?")
                    break
            else:
                raise ValueError(f"Unsupported condition format: {part}")

    # Construct the final filter condition with placeholders
    final_filter_condition = conditions[0]

    if default_params:
        default_idx = 0
        for idx, param in enumerate(sanitized_params):
            if param == "?":
                sanitized_params[idx] = default_params[default_idx]
                default_idx += 1

    for i in range(len(keywords)):
        final_filter_condition += f" {keywords[i]} {conditions[i + 1]}"

    return (
        final_filter_condition,
        tuple(sanitized_params),
    )


def filter_items(
    conn: sqlite3.Connection,
    table_name: str,
    attrs: list,
    object: object,
    keywords: list = None,
):
    """Given an object and a list of attributes, return filtered items."""

    filter_condition = []

    for attr in attrs:
        if hasattr(object, attr):
            value = getattr(object, attr)
            filter_condition.append(f"{attr} = {value}")

    if not keywords:
        # for idx, (keyword, cond) in enumerate(zip(keywords, filter_condition)):
        #     filter_condition[idx] =
        filter_condition = " AND ".join(filter_condition)

    return select_items(conn, table_name, filter_condition, type(object))


def get_column_names(cursor: sqlite3.Cursor, table_name: str):
    """
    Returns the columns of a table.
    """

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    return [col[1] for col in columns]


def insert_items(
    conn: sqlite3.Connection, table_name: str, objects: list, column_names: list = None
):
    """
    Insert data into an SQLite table.
    """
    if column_names and not isinstance(column_names, list):
        raise ValueError("'column_names' must be of type list.")

    if not isinstance(objects, list):
        raise ValueError("'objects' must be a list.")

    try:
        column_names = (
            get_column_names(conn.cursor, table_name)
            if column_names is None
            else column_names
        )
        placeholders = ", ".join(["?"] * len(column_names))
        columns = ", ".join(column_names)

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        last_row_id = None
        for object in objects:
            values = get_object_values(object, column_names)
            cursor, results = execute_query(conn, query, values, return_cursor=True)
            if cursor:
                last_row_id = cursor.lastrowid if cursor.lastrowid else last_row_id

        return last_row_id
    except sqlite3.Error as e:
        print("Error inserting data:", e)


def update_item(
    conn: sqlite3.Connection,
    table_name: str,
    obj: dict,
    filter_condition: str,
    updated_columns: list = None,
):
    """Update any given SQL object based on a filter condition."""

    try:

        if not isinstance(obj, dict):
            obj = vars(obj)

        if not updated_columns:
            updated_columns = obj.keys()

        set_clause = ", ".join([f"{column} = ?" for column in updated_columns])
        filter_condition, params = get_filter_condition(filter_condition)

        query = f"UPDATE {table_name} SET {set_clause} WHERE {filter_condition}"

        update_values = list(obj.values())
        update_values.extend(params)

        cursor, results = execute_query(conn, query, update_values, return_cursor=True)
        last_row_id = None
        if cursor:
            last_row_id = cursor.lastrowid if cursor.lastrowid else last_row_id
        return last_row_id
    except sqlite3.Error as e:
        print("Error updating data: ", e)
        return -1


def get_object_values(object, column_names: list):
    """Given a list of column names, returns the respective values for an object."""

    values = []

    for name in column_names:
        value = getattr(object, name)

        if (
            isinstance(value, list)
            or isinstance(value, tuple)
            or isinstance(value, dict)
        ):
            value = str(value)

        values.append(value)
    return values


def get_last_inserted_row_id(conn: sqlite3.Connection, table_name: str):
    """Returns last inserted row id."""

    query = f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
    result = execute_query(conn, query)
    return result[0][0] if len(result) > 0 else 0


def select_items(
    conn: sqlite3.Connection,
    table_name: str,
    filter_condition: str = None,
    mapped_object_type=None,
    column_names: list = [],
):
    """
    Retrieves a collection of items stored in the SQLite database.
    """
    query = f"SELECT * FROM {sanitize_values(table_name)[0]}"
    if filter_condition:
        filter_condition, params = get_filter_condition(filter_condition)

        query += f" WHERE {filter_condition}"
        results = execute_query(conn, query, params)
        # print(query, params)
    else:
        results = execute_query(conn, query)

    return (
        results
        if not mapped_object_type
        else map_sqlite_results_to_objects(results, mapped_object_type, column_names)
    )


def map_sqlite_results_to_objects(
    sqlite_results: list, object_type, column_names: list = []
):
    """Maps SQLite query results to a list of objects"""
    objects = []
    if len(column_names) > 0:
        for result in sqlite_results:
            o = object_type(*result)

            for name, result in zip(column_names, result):
                # check if result is array
                if (
                    isinstance(result, str)
                    and result.startswith("[")
                    and result.endswith("]")
                ):
                    result = literal_eval(result)
                if (
                    isinstance(result, str)
                    and result.startswith("{")
                    and result.endswith("}")
                ):
                    result = literal_eval(result)

                setattr(o, name, result)
            objects.append(o)
    else:
        objects = [object_type(*row) for row in sqlite_results]
    return objects


def delete_items(
    conn: sqlite3.Connection, table_name: str, filter_condition: str = "id = ?"
):
    """
    Deletes existing records from table.
    """
    query = f"DELETE FROM {table_name}"

    if filter_condition == "all":
        return execute_query(conn, query)
    else:
        filter_condition, params = get_filter_condition(filter_condition)
        query += f" WHERE {filter_condition}"
        return execute_query(conn, query, params)


def execute_query(
    conn: sqlite3.Connection, query: str, parameters: list = None, return_cursor=False
):
    """
    Execute an SQL query on the SQLite database.
    """

    results = []
    cursor = None

    try:
        cursor = conn.cursor()
        if parameters:
            # print(query, parameters)
            cursor.execute(query, parameters)
        else:
            # print(query)
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()

    except sqlite3.Error as e:
        print("Error executing query:", e)

    if return_cursor:
        return cursor, results

    return results


def create_table(conn: sqlite3.Connection, table_name: str, table_values: list):
    """
    Create a new SQLite table.
    """

    placeholders = ", ".join(table_values)
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({placeholders})"
    execute_query(conn, query)

    return table_name


def close_connection(conn: sqlite3.Connection):
    """
    Close the SQLite database connection.
    """

    if conn:
        conn.close()


def get_random_row(
    conn: sqlite3.Connection, table_name: str, mapped_object_type: type = None
):
    """
    Returns a random row in the SQLite database, if it exists.
    """

    table_name = sanitize_values(table_name)[0]
    results = execute_query(
        conn, "SELECT * FROM {} ORDER BY RANDOM() LIMIT 1".format(table_name)
    )
    return (
        results
        if mapped_object_type is None
        else map_sqlite_results_to_objects(results, mapped_object_type)
    )
