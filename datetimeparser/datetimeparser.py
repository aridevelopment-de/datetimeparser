"""
Main module which provides the parse function.
"""

__all__ = ['parse', '__version__', '__author__']
__version__ = "0.13.5"
__author__ = "aridevelopment"

import datetime
from typing import Optional

from datetimeparser.evaluator import Evaluator
from datetimeparser.parser import Parser


def parse(
        datetime_string: str,
        timezone: str = "Europe/Berlin",
        coordinates: Optional[tuple[float, float]] = None
) -> Optional[tuple[datetime.datetime, str, tuple[float, float]]]:
    """
    Parses a datetime string and returns a datetime object.
    If the datetime string cannot be parsed, None is returned.

    :param datetime_string: The datetime string to parse.
    :param timezone: The timezone to use. Should be a valid timezone for pytz.timezone(). Default: Europe/Berlin
    :param coordinates: A tuple containing longitude and latitude. If coordinates are given, the timezone will be calculated,
        independently of the given timezone param
        NOTE: It takes a longer time to calculate the timezone, it can happen that it takes up to 30 seconds for a result
    :return: A datetime object or None
    """
    parser_result = Parser(datetime_string).parse()

    if parser_result is None:
        return None

    evaluator_result, tz, coords = Evaluator(parser_result, tz=timezone, coordinates=coordinates).evaluate()

    if evaluator_result is None:
        return None

    return evaluator_result, tz, coords
