from pytz import timezone, UnknownTimeZoneError

from .evaluatormethods import *


class Evaluator:
    def __init__(self, parsed_object, tz="Europe/Berlin"):
        try:
            tiz = timezone(tz)
        except UnknownTimeZoneError:
            raise ValueError("Unknown timezone: {}".format(tz))

        self.parsed_object_type = parsed_object[0]
        self.parsed_object_content: Union[list, AbsoluteDateTime, RelativeDateTime] = parsed_object[1]
        self.current_datetime: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=tiz), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    def evaluate(self) -> Union[datetime, int, None]:
        ev_out = None

        if self.parsed_object_type == Method.ABSOLUTE_DATE_FORMATS:
            ev_out = evaluate_absolute_date_formats(
                self.current_datetime,
                self.parsed_object_content
            )

        if self.parsed_object_type == Method.ABSOLUTE_PREPOSITIONS:
            ev_out = evaluate_absolute_prepositions(
                self.current_datetime,
                self.parsed_object_content
            )

        if self.parsed_object_type == Method.CONSTANTS:
            ev_out = evaluate_constants(
                self.current_datetime,
                self.parsed_object_content
            )

            if not isinstance(ev_out, AbsoluteDateTime):
                return ev_out

        if self.parsed_object_type == Method.RELATIVE_DATETIMES:
            ev_out = evaluate_relative_datetime(
                self.current_datetime,
                self.parsed_object_content
            )

        if self.parsed_object_type == Method.CONSTANTS_RELATIVE_EXTENSIONS:
            ev_out = evaluate_constant_relatives(
                self.current_datetime,
                self.parsed_object_content
            )

        if self.parsed_object_type == Method.DATETIME_DELTA_CONSTANTS:
            ev_out = evaluate_datetime_delta_constants(
                self.current_datetime,
                self.parsed_object_content
            )

        if isinstance(ev_out, datetime):
            return ev_out
        try:
            dt_object = datetime(
                ev_out.year,
                ev_out.month,
                ev_out.day,
                ev_out.hour,
                ev_out.minute,
                ev_out.second
            )
            return dt_object
        except ValueError:
            return None
