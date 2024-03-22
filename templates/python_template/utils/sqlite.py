import sqlite3
from ast import literal_eval
import re


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

    if not isinstance(values, list):
        values = [values]

    for i, value in enumerate(values):
        if not get_date_format(value):
            values[i] = re.sub(expression, "", value)
    return values


# filter condition modification


def sanitize_filter_condition(filter_condition: str):
    """
    Sanitizes filter condition of type id = '1'. Returns the filter condition keys and a tuple of sanitized parameters.
    """

    if not isinstance(filter_condition, str):
        raise ValueError("filter_condition must be of type str.")

    filter_condition_keys = []
    sanitized_params = []

    conditions = filter_condition.split("AND")

    for condition in conditions:
        key, value = condition.split("=")

        key = key.strip()
        value = value.strip()

        filter_condition_keys.append(key)
        sanitized_params.extend(sanitize_values(value))

    return filter_condition_keys, tuple(sanitized_params)


def get_filter_condition(keys: list):

    filter_condition = []

    for key in keys:
        filter_condition.append(f"{key} = ?")

    filter_condition = " AND ".join(filter_condition)

    return filter_condition


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
        cursor = conn.cursor()
        column_names = (
            get_column_names(cursor, table_name)
            if column_names is None
            else column_names
        )
        print(table_name)
        placeholders = ", ".join(["?"] * len(column_names))
        columns = ", ".join(column_names)

        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for object in objects:
            values = get_object_values(object, column_names)
            cursor.execute(query, values)
            conn.commit()

        return cursor.lastrowid
    except sqlite3.Error as e:
        print("Error inserting data:", e)
        return None


def update_item(
    conn: sqlite3.Connection,
    table_name: str,
    obj: dict,
    filter_condition: str,
    updated_columns: list = None,
):
    """Update any given SQL object based on a filter condition."""

    try:
        cursor = conn.cursor()

        if not isinstance(obj, dict):
            obj = vars(obj)

        if not updated_columns:
            updated_columns = obj.keys()

        set_clause = ", ".join([f"{column} = ?" for column in updated_columns])
        query = f"UPDATE {table_name} SET {set_clause} WHERE {filter_condition}"

        update_values = tuple(obj.values())
        cursor.execute(query, update_values)
        conn.commit()

        return cursor.lastrowid

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
        filter_condition_keys, params = sanitize_filter_condition(filter_condition)
        filter_condition_keys: list
        filter_condition = get_filter_condition(filter_condition_keys)

        query += f" WHERE {filter_condition}"
        print(query)
        results = execute_query(conn, query, params)
    else:
        results = execute_query(conn, query)

    return (
        results
        if not mapped_object_type
        else map_sqlite_results_to_objects(results, mapped_object_type, column_names)
    )


def select_random_item(
    conn: sqlite3.Connection,
    table_name: str,
    mapped_object_type=None,
    column_names: list = [],
):
    """
    Returns a random item stored in the SQLite database, if it exists.
    """

    query = f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1"
    results = execute_query(conn, query)

    return (
        results
        if mapped_object_type is None
        else map_sqlite_results_to_objects(results, mapped_object_type, column_names)
    )


def map_sqlite_results_to_objects(
    sqlite_results: list, object_type, column_names: list = []
):
    """Maps SQLite query results to a list of objects"""
    objects = []
    if len(column_names) > 0:
        for result in sqlite_results:
            o = object_type()

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
        filter_condition, params = sanitize_filter_condition(filter_condition)
        query += f" WHERE {get_filter_condition(filter_condition)}"
        return execute_query(conn, query, params)


def execute_query(conn: sqlite3.Connection, query: str, parameters: list = None):
    """
    Execute an SQL query on the SQLite database.
    """

    try:
        cursor = conn.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        return results
    except sqlite3.Error as e:
        print("Error executing query:", e)
        return []


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


def get_random_row(conn: sqlite3.Connection, table_name: str):
    """
    Returns random row of SQLite database table.
    """
    table_name = sanitize_values(table_name)[0]
    # print(table_name)
    return execute_query(
        conn, "SELECT * FROM {} ORDER BY RANDOM() LIMIT 1".format(table_name)
    )
