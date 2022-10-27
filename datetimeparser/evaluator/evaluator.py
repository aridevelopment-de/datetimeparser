from datetime import datetime
from pytz import timezone, UnknownTimeZoneError
from typing import Optional, Union

from datetimeparser.utils.baseclasses import AbsoluteDateTime, RelativeDateTime
from datetimeparser.utils.enums import Method
from datetimeparser.evaluator.evaluatormethods import EvaluatorMethods
from datetimeparser.utils.exceptions import FailedEvaluation, InvalidValue
from datetimeparser.utils.geometry import TimeZoneManager


class Evaluator:
    def __init__(self, parsed_object, tz="Europe/Berlin", coordinates: Optional[tuple[float, float]] = None):
        """
        :param parsed_object: the parsed object from parser
        :param tz: the timezone for the datetime
        :param coordinates: longitude and latitude for timezone calculation and for sunrise and sunset
        """

        if coordinates:
            tz = TimeZoneManager().timezone_at(lng=coordinates[0], lat=coordinates[1])
        try:
            tiz = timezone(tz)
        except UnknownTimeZoneError:
            raise InvalidValue(f"Unknown timezone: '{tz}'")

        self.parsed_object_type = parsed_object[0]
        self.parsed_object_content: Union[list, AbsoluteDateTime, RelativeDateTime] = parsed_object[1]
        self.current_datetime: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=tiz), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        self.offset = tiz.utcoffset(self.current_datetime)
        self.timezone = tiz
        self.coordinates = coordinates

    def evaluate(self) -> Union[tuple[datetime, str, tuple[float, float]], None]:
        ev_out = None
        ev = EvaluatorMethods(self.parsed_object_content, self.current_datetime, self.coordinates, self.timezone.zone, self.offset)

        if self.parsed_object_type == Method.ABSOLUTE_DATE_FORMATS:
            ev_out = ev.evaluate_absolute_date_formats()

        if self.parsed_object_type == Method.ABSOLUTE_PREPOSITIONS:
            ev_out = ev.evaluate_absolute_prepositions()

        if self.parsed_object_type == Method.CONSTANTS:
            ev_out = ev.evaluate_constants()

        if self.parsed_object_type == Method.RELATIVE_DATETIMES:
            ev_out = ev.evaluate_relative_datetime()

        if self.parsed_object_type == Method.CONSTANTS_RELATIVE_EXTENSIONS:
            ev_out = ev.evaluate_constant_relatives()

        if self.parsed_object_type == Method.DATETIME_DELTA_CONSTANTS:
            ev_out = ev.evaluate_datetime_delta_constants()

        if ev_out:
            return ev_out, self.timezone.zone, self.coordinates
        else:
            raise FailedEvaluation(self.parsed_object_content)
