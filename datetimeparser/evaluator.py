from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union
from pytz import timezone

from .enums import *
from .baseclasses import *


def eastern_calc(year_time: int) -> datetime:
    a = year_time % 19
    k = year_time // 100
    m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
    d = (19 * a + m) % 30
    s = 2 - (3 * k + 3) // 4
    r = d // 29 + (d // 28 - d // 29) * (a // 11)
    og = 21 + d + r
    sz = 7 - (year_time + year_time // 4 + s) % 7
    oe = 7 - (og - sz) % 7
    os = og + oe

    if os > 32:
        return datetime(year=year_time, month=4, day=(os-31))
    else:
        return datetime(year=year_time, month=3, day=os)


def thanksgiving_calc(year_time: int) -> datetime:
    year_out = datetime(year=year_time, month=11, day=29)
    date_out = datetime(year=year_time, month=11, day=3)
    return year_out - timedelta(days=(date_out.weekday() + 2))


def days_feb(year_time: int) -> int:
    if int(year_time) % 400 == 0 or int(year_time) % 4 == 0 and not int(year_time) % 100 == 0:
        return 29
    else:
        return 28


def year(year_time: int) -> datetime:
    return datetime(year=year_time, month=1, day=1)


class Evaluator:
    CURRENT_DATE: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=timezone("Europe/Berlin")), "%Y-%m-%d"), "%Y-%m-%d")
    CURRENT_DATETIME: datetime = datetime.strptime(datetime.strftime(datetime.now(tz=timezone("Europe/Berlin")), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    EVENTS = {
        "silvester": lambda year_time: datetime(year=year_time, month=12, day=31),
        "nicholas": lambda year_time: datetime(year=year_time, month=12, day=6),
        "christmas": lambda year_time: datetime(year=year_time, month=12, day=25),
        "halloween": lambda year_time: datetime(year=year_time, month=10, day=31),
        "april fools day": lambda year_time: datetime(year=year_time, month=4, day=1),
        "eastern": eastern_calc,
        "thanksgiving": thanksgiving_calc,
        "saint patrick's day": lambda year_time: datetime(year=year_time, month=3, day=17),
        "valentines day": lambda year_time: datetime(year=year_time, month=2, day=14),

        # meteorological dates, if someone has any problem with that... -> fork this project, build a function for that and create a pull request :)
        "spring begin": lambda year_time: datetime(year=year_time, month=3, day=1),
        "spring end": lambda year_time: datetime(year=year_time, month=5, day=31, hour=23, minute=59, second=59),
        "summer begin": lambda year_time: datetime(year=year_time, month=6, day=1),
        "summer end": lambda year_time: datetime(year=year_time, month=8, day=31, hour=23, minute=59, second=59),
        "fall begin": lambda year_time: datetime(year=year_time, month=9, day=1),
        "fall end": lambda year_time: datetime(year=year_time, month=11, day=30, hour=23, minute=59, second=59),
        "winter begin": lambda year_time: datetime(year=year_time, month=12, day=1),
        "winter end": lambda year_time: datetime(year=year_time, month=2, day=days_feb(year_time), hour=23, minute=59, second=59),

        "aoc begin": lambda year_time: datetime(year=year_time, month=12, day=1, hour=6),
        "aoc end": lambda year_time: datetime(year=year_time, month=12, day=26, hour=6),

        "end of year": lambda year_time: datetime(year=year_time, month=12, day=31, hour=23, minute=59, second=59),

        "infinity": -1
    }

    DAYS = {
        "monday": f"{CURRENT_DATE + timedelta((0 - CURRENT_DATE.weekday()) % 7)}",
        "tuesday": f"{CURRENT_DATE + timedelta((1 - CURRENT_DATE.weekday()) % 7)}",
        "wednesday": f"{CURRENT_DATE + timedelta((2 - CURRENT_DATE.weekday()) % 7)}",
        "thursday": f"{CURRENT_DATE + timedelta((3 - CURRENT_DATE.weekday()) % 7)}",
        "friday": f"{CURRENT_DATE + timedelta((4 - CURRENT_DATE.weekday()) % 7)}",
        "saturday": f"{CURRENT_DATE + timedelta((5 - CURRENT_DATE.weekday()) % 7)}",
        "sunday": f"{CURRENT_DATE + timedelta((6 - CURRENT_DATE.weekday()) % 7)}"
    }

    MONTHS = {
        "january": lambda year_time: datetime(year=year_time, month=1, day=1),
        "february": lambda year_time: datetime(year=year_time, month=2, day=1),
        "march": lambda year_time: datetime(year=year_time, month=3, day=1),
        "april": lambda year_time: datetime(year=year_time, month=4, day=1),
        "may": lambda year_time: datetime(year=year_time, month=5, day=1),
        "june": lambda year_time: datetime(year=year_time, month=6, day=1),
        "july": lambda year_time: datetime(year=year_time, month=7, day=1),
        "august": lambda year_time: datetime(year=year_time, month=8, day=1),
        "september": lambda year_time: datetime(year=year_time, month=9, day=1),
        "october": lambda year_time: datetime(year=year_time, month=10, day=1),
        "november": lambda year_time: datetime(year=year_time, month=11, day=1),
        "december": lambda year_time: datetime(year=year_time, month=12, day=1)
    }

    def __init__(self, parsed_object: list):
        self.parsed_object_type = parsed_object[0]
        self.parsed_object_content: Union[list, AbsoluteDateTime, RelativeDateTime] = parsed_object[1]

    def evaluate(self) -> Union[datetime, int, None]:
        ev_out = AbsoluteDateTime()

        if self.parsed_object_type == Method.ABSOLUTE_DATE_FORMATS:

            parsed_time: AbsoluteDateTime = self.parsed_object_content

            ev_out.year = self.CURRENT_DATETIME.year if parsed_time.year == 0 else parsed_time.year
            ev_out.month = self.CURRENT_DATETIME.month if parsed_time.month == 0 else parsed_time.month
            ev_out.day = self.CURRENT_DATETIME.day if parsed_time.day == 0 else parsed_time.day
            ev_out.hour = parsed_time.hour
            ev_out.minute = parsed_time.minute
            ev_out.second = parsed_time.second

        if self.parsed_object_type == Method.ABSOLUTE_PREPOSITIONS:
            pass

        if self.parsed_object_type == Method.CONSTANTS:

            dt: datetime = self.CURRENT_DATETIME

            if len(self.parsed_object_content) == 2:

                if isinstance(self.parsed_object_content[0], Constant):
                    object_type: Constant = self.parsed_object_content[0]
                    object_year: AbsoluteDateTime = self.parsed_object_content[1].year
                    dt = self.EVENTS[str(object_type.name)](object_year)
                    if self.CURRENT_DATETIME > dt and object_year == 0:
                        dt += relativedelta(years=1)

            else:
                if self.parsed_object_content[0].name in self.EVENTS:
                    if self.parsed_object_content[0].name == "infinity":
                        return self.EVENTS["infinity"]
                    dt = self.EVENTS[str(self.parsed_object_content[0].name)](self.CURRENT_DATETIME.year)
                    if self.CURRENT_DATETIME > dt:
                        dt += relativedelta(years=1)
                elif self.parsed_object_content[0].name in self.DAYS:
                    dt = datetime.strptime(f"{self.DAYS[str(self.parsed_object_content[0].name)].format(self.CURRENT_DATETIME.year)}", "%Y-%m-%d %H:%M:%S")
            ev_out.year, ev_out.month, ev_out.day = dt.year, dt.month, dt.day
            ev_out.hour, ev_out.minute, ev_out.second = dt.hour, dt.minute, dt.second

        if self.parsed_object_type == Method.RELATIVE_DATETIMES:

            new = self.CURRENT_DATETIME

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
            now: datetime = self.CURRENT_DATE

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
