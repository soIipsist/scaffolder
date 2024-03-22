from utils.sqlite import create_connection, create_table, close_connection, delete_items
from constants import *
import os


def create_db(db_path: str = db_path, tables: list = tables, values: list = values):

    print("Creating database...")

    conn = create_connection(db_path)
    # create tables
    for t, v in zip(tables, values):
        create_table(conn, t, v)

    return conn


def rebuild_db():
    delete_db()
    conn = create_connection(db_path)
    for t, v in zip(tables, values):
        create_table(conn, t, v)
        delete_items(conn, t, "all")


def reset_db(conn):
    for t in tables:
        delete_items(conn, t, "all")


def delete_db(conn):
    close_connection(conn)
    try:
        os.remove(db_path)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    create_db()
