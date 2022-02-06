import datetime
from typing import Union

from datetimeparser.Parser import Parser
from datetimeparser.Evaluator import Evaluator


def parse(datetime_string) -> Union[datetime.datetime, int, None]:
    """
    Parses a datetime string and returns a datetime object.
    There are special cases where an integer is returned instead.
    These currently consist of:
    - Infinity

    If the datetime string cannot be parsed, None is returned.

    :param datetime_string: The datetime string to parse.
    :return: A datetime object or an integer.
    """
    parser_result = Parser(datetime_string).parse()

    if parser_result is None:
        return None

    evaluator_result = Evaluator(parser_result).evaluate()

    if evaluator_result is None:
        return None

    return evaluator_result
