import datetime
from typing import Union

from datetimeparser.evaluator import Evaluator
from datetimeparser.parser import Parser


def parse(datetime_string: str, timezone: str = "Europe/Berlin") -> Union[datetime.datetime, int, None]:
    """
    Parses a datetime string and returns a datetime object.
    -1 is returned if the result is Infinity.
    If the datetime string cannot be parsed, None is returned.

    :param datetime_string: The datetime string to parse.
    :param timezone: The timezone to use. Should be a valid timezone for pytz.timezone(). Default: Europe/Berlin
    :return: A datetime object or an integer or None
    """
    parser_result = Parser(datetime_string).parse()

    if parser_result is None:
        return None

    evaluator_result = Evaluator(parser_result, tz=timezone).evaluate()

    if evaluator_result is None:
        return None

    return evaluator_result
