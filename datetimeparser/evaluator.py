from dateutil.relativedelta import relativedelta
from pytz import timezone, UnknownTimeZoneError
from typing import Union

from .baseclasses import *
from .enums import *


class Evaluator:
    def __init__(self, parsed_object, tz="Europe/Berlin"):
        try:
            tiz = timezone(tz)
        except UnknownTimeZoneError:
            raise ValueError("Unknown timezone: {}".format(tz))

        self.parsed_object_type = parsed_object[0]
        self.parsed_object_content: Union[list, AbsoluteDateTime, RelativeDateTime] = parsed_object[1]
        self.current_date: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=tiz), "%Y-%m-%d"), "%Y-%m-%d")
        self.current_datetime: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=tiz), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    def evaluate(self) -> Union[datetime, int, None]:
        ev_out = AbsoluteDateTime()

        if self.parsed_object_type == Method.ABSOLUTE_DATE_FORMATS:
            parsed_time: AbsoluteDateTime = self.parsed_object_content

            ev_out.year = self.current_datetime.year if parsed_time.year == 0 else parsed_time.year
            ev_out.month = self.current_datetime.month if parsed_time.month == 0 else parsed_time.month
            ev_out.day = self.current_datetime.day if parsed_time.day == 0 else parsed_time.day
            ev_out.hour = parsed_time.hour
            ev_out.minute = parsed_time.minute
            ev_out.second = parsed_time.second

        if self.parsed_object_type == Method.ABSOLUTE_PREPOSITIONS:
            pass

        if self.parsed_object_type == Method.CONSTANTS:
            dt: datetime = self.current_datetime

            if len(self.parsed_object_content) == 2:
                if isinstance(self.parsed_object_content[0], Constant):
                    object_type: Constant = self.parsed_object_content[0]
                    object_year: AbsoluteDateTime = self.parsed_object_content[1].year
                    dt = object_type.time_value(object_year)

                    if self.current_datetime > dt and object_year == 0:
                        dt += relativedelta(years=1)

            else:
                object_type: Constant = self.parsed_object_content[0]

                if object_type.name == "infinity":
                    return object_type.value

                elif object_type in WeekdayConstants.ALL:
                    return object_type.time_value(self.current_datetime)

                dt = object_type.time_value(self.current_datetime.year)
                if self.current_datetime > dt:
                    dt += relativedelta(years=1)

            ev_out.year, ev_out.month, ev_out.day = dt.year, dt.month, dt.day
            ev_out.hour, ev_out.minute, ev_out.second = dt.hour, dt.minute, dt.second

        if self.parsed_object_type == Method.RELATIVE_DATETIMES:
            new = self.current_datetime

            new += relativedelta(
                years=self.parsed_object_content.years,
                months=self.parsed_object_content.months,
                weeks=self.parsed_object_content.weeks,
                days=self.parsed_object_content.days,
                hours=self.parsed_object_content.hours,
                minutes=self.parsed_object_content.minutes,
                seconds=self.parsed_object_content.seconds
            )

            ev_out.year, ev_out.month, ev_out.day = new.year, new.month, new.day
            ev_out.hour, ev_out.minute, ev_out.second = new.hour, new.minute, new.second

        if self.parsed_object_type == Method.DATETIME_DELTA_CONSTANTS:
            relative_time: RelativeDateTime = self.parsed_object_content
            now: datetime = self.current_date

            ev_out.year, ev_out.month, ev_out.day = now.year, now.month, now.day
            ev_out.hour, ev_out.minute, ev_out.second = relative_time.hours, relative_time.minutes, relative_time.seconds

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
