"""
Main module which provides the parse function.
"""

__all__ = ['parse', 'Result', '__version__', '__author__']
__version__ = "0.14.0"
__author__ = "aridevelopment"

from typing import Optional

from datetimeparser.evaluator import Evaluator
from datetimeparser.parser import Parser
from datetimeparser.utils.models import Result


def parse(
        datetime_string: str,
        timezone: str = "Europe/Berlin",
        coordinates: Optional[tuple[float, float]] = None
) -> Optional[Result]:
    """
    Parses a datetime string and returns a datetime object.
    If the datetime string cannot be parsed, None is returned.

    :param datetime_string: The datetime string to parse.
    :param timezone: The timezone to use. Should be a valid timezone for pytz.timezone(). Default: Europe/Berlin
    :param coordinates: A tuple containing longitude and latitude. If coordinates are given, the timezone will be calculated,
        independently of the given timezone param.
        NOTE: It can take some seconds until a result is returned
    :return: A result object containing the returned time, the timezone and optional coordinates.
             If the process fails, None will be returned
    """
    parser_result = Parser(datetime_string).parse()

    if parser_result is None:
        return None

    evaluator_result, tz, coordinates = Evaluator(parser_result, tz=timezone, coordinates=coordinates).evaluate()

    if evaluator_result is None:
        return None

    return Result(evaluator_result, tz, coordinates)
