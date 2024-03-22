import questionary
from prompt_toolkit.document import Document
import re


def get_empty_question_attributes(object, attr_names: list):
    return [name for name in attr_names if not getattr(object, name)]


def get_question_choices(choice_texts: list, choice_values: list):

    choices = []
    for t, v in zip(choice_texts, choice_values):
        choices.append(questionary.Choice(title=t, value=v))

    return choices


def get_questions_from_sqlite_object(
    object, attr_names: list = [], get_empty_attributes: bool = False
):

    if not attr_names:
        attr_names = object.column_names

    if get_empty_attributes:
        attr_names = get_empty_question_attributes(object, attr_names)

    questions = []

    attr_names = [name for name in attr_names if name in object.column_names]

    for name in attr_names:

        question_dict = {}
        object_key = name
        question_dict = object.question_arguments.get(name)
        object_value = getattr(object, object_key)  # gets value inside object

        question_dict = get_question(question_dict, object_key, object_value)
        questions.append(question_dict)

    return questions


def get_question(question_dict: dict, object_key: str = None, object_value: str = None):
    questionary_actions = {int: "text", str: "text", list: "select"}

    questionary_validators = {
        "int_validator": TypeValidator(int),
        "date_validator": DateValidator(),
        "float_validator": TypeValidator(float),
        "time_validator": TimeValidator(),
        "time_range_validator": TimeRangeValidator(),
        "target_int_validator": TargetIntValidator(),
        "target_float_validator": TargetFloatValidator(),
    }

    question_message = question_dict.get(
        "message", object_key if object_key else "message"
    )
    question_type = question_dict.get(
        "type", questionary_actions.get(type(object_value), "text")
    )

    validator = question_dict.get("validate")
    question_name = object_key if object_key else "q1"

    # get validator
    if validator and isinstance(validator, str):
        validator = questionary_validators.get(validator, "int_validator")
        question_dict.update({"validate": validator})

    question_dict.update(
        {"type": question_type, "message": question_message, "name": question_name}
    )

    # add choices if 'select' type
    if question_type == "select" and not "choices" in question_dict:
        choices_val = (
            object_value
            if isinstance(object_value, list) and len(object_value) > 0
            else ["Select", "Update"]
        )
        question_dict.update({"choices": choices_val})

    # set default value
    if object_value:
        question_dict.update({"default": object_value})

    return question_dict


def prompt_questions(questions: list, object=None, question_names: list = []):

    if not questions:
        return []

    if isinstance(questions, dict):
        questions = [questions]

    if question_names:
        questions = [
            question for question in questions if question.get("name") in question_names
        ]

    answers = questionary.prompt(questions)

    if object:
        for k, v in answers.items():
            setattr(object, k, v)

    return answers


class DateValidator(questionary.Validator):

    def validate(self, document: Document) -> None:
        from templates.python_template.utils.date_utils import parse_date

        try:
            parse_date(document.text)
        except Exception as e:
            raise questionary.ValidationError(
                message=f"Please enter a valid date.",
                cursor_position=len(document.text),
            )


class TypeValidator(questionary.Validator):
    def __init__(self, type=int) -> None:
        self.type = type
        super().__init__()

    def validate(self, document):

        try:
            self.type(document.text)
        except Exception as e:
            raise questionary.ValidationError(
                message=f"Please enter a valid {self.type.__name__} value.",
                cursor_position=len(document.text),
            )


class TimeValidator(questionary.Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, document: Document) -> None:
        from templates.python_template.utils.date_utils import parse_time

        try:
            parse_time(document.text)
        except Exception as e:
            raise questionary.ValidationError(
                message=f"Please enter a valid time.",
                cursor_position=len(document.text),
            )


class TimeRangeValidator(questionary.Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, document: Document) -> None:
        from templates.python_template.utils.date_utils import parse_time_range

        try:
            parse_time_range(document.text)
        except Exception as e:
            raise questionary.ValidationError(
                message=f"Please enter a valid time range.",
                cursor_position=len(document.text),
            )


class TargetIntValidator(questionary.Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, document: Document) -> None:

        matches = re.match(r"^\d+/\d+$", document.text)
        if not matches:
            raise questionary.ValidationError(
                message=f"Please enter a valid target.",
                cursor_position=len(document.text),
            )


class TargetFloatValidator(questionary.Validator):
    def __init__(self) -> None:
        super().__init__()

    def validate(self, document: Document) -> None:
        matches = re.match(r"^\d+(\.\d+)?/\d+(\.\d+)?$", document.text)

        if not matches:
            raise questionary.ValidationError(
                message=f"Please enter a valid target.",
                cursor_position=len(document.text),
            )
