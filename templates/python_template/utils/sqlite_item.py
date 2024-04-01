from utils.file_operations import read_file, overwrite_file
from utils.sqlite import (
    select_items,
    update_item,
    insert_items,
    delete_items,
    get_filter_condition,
    create_connection,
    sanitize_filter_condition,
    filter_items,
)
import re
from constants import db_path
import os

conn = create_connection(db_path)


class SQLiteItem:

    error_message = None

    def __init__(self, table_values: list, column_names: list = None) -> None:
        self.table_name = self.__class__.__name__
        self.table_values = table_values
        self.column_names = (
            column_names if column_names else self.get_column_names_from_table()
        )
        self.error_message = f"{self.__class__.__name__} does not exist"

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

    def select(self):
        items = select_items(
            conn,
            self.table_name,
            self.filter_condition,
            type(self),
            column_names=self.column_names,
        )
        return items[0] if len(items) > 0 else None

    def filter(self, attrs: list = []):
        if attrs:
            return filter_items(conn, self.table_name, attrs, self)
        else:
            return self.select_all()

    def select_all(self):
        return select_items(conn, self.table_name, None, type(self), self.column_names)

    def insert(self):
        return insert_items(conn, self.table_name, [self], self.column_names)

    def update(self):
        obj = self.get_unique_object()
        return update_item(conn, self.table_name, obj, self.filter_condition)

    def delete(self):
        delete_items(conn, self.table_name, self.filter_condition)

    # item operations

    def get_item(self):
        item = self.select()

        if not item:
            print(self.error_message)
        else:
            item: SQLiteItem
            item.filter_condition = self.filter_condition
        return item

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
