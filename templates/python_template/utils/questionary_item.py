from utils.sqlite_item import SQLiteItem
import questionary

class QuestionaryItem(SQLiteItem):
    question_arguments:dict = {}
    q_args:list = []
    
    def __init__(self, table_values: list, column_names: list = None) -> None:
        super().__init__(table_values, column_names)