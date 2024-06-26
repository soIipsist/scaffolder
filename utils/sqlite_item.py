import re
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parent_directory)

from utils.sqlite_connection import db_path
from utils.file_utils import read_file, overwrite_file
from utils.sqlite import (
    select_items,
    update_item,
    insert_items,
    delete_items,
    create_connection,
    filter_items,
    get_random_row,
)

conn = create_connection(db_path)


class SQLiteItem:

    logging = True
    log_message = None

    def __init__(self, table_values: list, column_names: list = None) -> None:
        self.table_name = self.__class__.__name__
        self.table_values = table_values
        self.column_names = (
            column_names if column_names else self.get_column_names_from_table()
        )
        self.logging = False
        self._filter_condition = None

    @property
    def filter_condition(self):
        return self._filter_condition

    @filter_condition.setter
    def filter_condition(self, new_filter_condition):
        self._filter_condition = new_filter_condition

    # sqlite operations

    def get_unique_object(self):
        sqlite_item = SQLiteItem(self.table_values, self.column_names)
        sqlite_keys = list(vars(sqlite_item).keys())

        dictionary: dict = vars(self)
        temp_dict = dictionary.copy()

        for key in dictionary:
            if key in sqlite_keys or key.startswith("_"):
                temp_dict.pop(key)

        return temp_dict

    def get_default_attr_names(self):
        return [name for name in self.column_names if name != "id"]

    def get_column_names_from_table(self):
        return [v.split(" ")[0] for v in self.table_values]

    def get_object_values(self, attr_names: list = []):

        if not attr_names:
            attr_names = self.column_names

        return [getattr(self, name) for name in attr_names]

    def filter_by(self, attrs: list = None):
        if attrs:
            return filter_items(conn, self.table_name, attrs, self)
        else:
            return self.select_all()

    def select(self, filter_condition=None):

        condition = (
            self.filter_condition if filter_condition is None else filter_condition
        )

        items = select_items(
            conn,
            self.table_name,
            condition,
            type(self),
            column_names=self.column_names,
        )

        return items

    def select_all(self):
        return select_items(conn, self.table_name, None, type(self), self.column_names)

    def insert(self):
        return insert_items(conn, self.table_name, [self], self.column_names)

    def update(self, filter_condition=None):
        obj = self.get_unique_object()
        condition = (
            self.filter_condition if filter_condition is None else filter_condition
        )

        return update_item(conn, self.table_name, obj, condition)

    def delete(self, filter_condition=None):

        condition = (
            self.filter_condition if filter_condition is None else filter_condition
        )
        return delete_items(conn, self.table_name, condition)

    def export_item(self, path: str):
        content = self.__str__()
        overwrite_file(path, content, encoding="utf-8")

    def import_item(
        self, path: str, regex: list = [], attr_names: list = [], insert=True
    ):

        content = read_file(path)

        attr_names = [name for name in attr_names if name in self.column_names]

        if len(regex) != len(attr_names):
            raise ValueError("regex array length not equal to attr_names.")

        for r, name in zip(regex, attr_names):
            match = re.findall(r, content)[0]
            print(f"Found match to regex {r}: {match}")
            setattr(self, name, match)

        if insert:
            self.insert()

    def get_random_item(self):
        item = get_random_row(conn, self.table_name, type(self))
        return item

    def log(self, log_message: str = None):

        if self.logging and log_message:
            log_message = log_message if log_message else self.log_message
            print(log_message)
