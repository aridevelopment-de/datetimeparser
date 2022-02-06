from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union
from pytz import timezone

from .baseclasses import *


def eastern_calc(year_time: int) -> str:
    A = year_time % 19
    K = year_time // 100
    M = 15 + (3 * K + 3) // 4 - (8 * K + 13) // 25
    D = (19 * A + M) % 30
    S = 2 - (3 * K + 3) // 4
    R = D // 29 + (D // 28 - D // 29) * (A // 11)
    OG = 21 + D + R
    SZ = 7 - (year_time + year_time // 4 + S) % 7
    OE = 7 - (OG - SZ) % 7
    OS = OG + OE

    if OS > 32:
        return f"{year_time}-04-{OS-31} 0:00:00"
    else:
        return f"{year_time}-03-{OS} 0:00:00"


def thanksgiving_calc(year_time: int) -> datetime:
    year_out = datetime.strptime(f"{year_time}-11-29 0:00:00", "%Y-%m-%d %H:%M:%S")
    date_out = datetime.strptime(f"{year_time}-11-3 0:00:00", "%Y-%m-%d %H:%M:%S")
    return year_out - timedelta(days=(date_out.weekday() + 2))


def days_feb(year_time: int) -> str:
    if int(year_time) % 400 == 0 or int(year_time) % 4 == 0 and not int(year_time) % 100 == 0:
        return "29"
    else:
        return "28"


def year(year_time: int) -> str:
    return f"{year_time}-01-01 0:00:00"


class Evaluator:
    CURRENT_DATE = datetime.strptime(datetime.strftime(datetime.now(tz=timezone("Europe/Berlin")), "%Y-%m-%d"), "%Y-%m-%d")
    CURRENT_DATETIME = datetime.strptime(datetime.strftime(datetime.now(tz=timezone("Europe/Berlin")), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    EVENTS = {
        "silvester": lambda year_time: f"{year_time}-12-31 0:00:00",
        "nicholas": lambda year_time: f"{year_time}-12-06 0:00:00",
        "christmas": lambda year_time: f"{year_time}-12-25 0:00:00",
        "halloween": lambda year_time: f"{year_time}-10-31 0:00:00",
        "april fools day": lambda year_time: f"{year_time}-04-01 0:00:00",
        "eastern": eastern_calc,
        "thanksgiving": thanksgiving_calc,
        "saint patrick's day": lambda year_time: f"{year_time}-03-17 0:00:00",
        "valentines day": lambda year_time: f"{year_time}-02-14 0:00:00",

        # meteorological dates, if someone has any problem with that... -> fork this project, build a function for that and create a pull request :)
        "spring begin": lambda year_time: f"{year_time}-03-01 0:00:00",
        "spring end": lambda year_time: f"{year_time}-05-31 23:59:59",
        "summer begin": lambda year_time: f"{year_time}-06-01 0:00:00",
        "summer end": lambda year_time: f"{year_time}-08-31 23:59:59",
        "fall begin": lambda year_time: f"{year_time}-09-01 0:00:00",
        "fall end": lambda year_time: f"{year_time}-11-30 23:59:59",
        "winter begin": lambda year_time: f"{year_time}-12-01 0:00:00",
        "winter end": lambda year_time: f"{year_time}-02-{days_feb(year_time)} 23:59:59",

        "aoc begin": lambda year_time: f"{year_time}-12-01 6:00:00",
        "aoc end": lambda year_time: f"{year_time}-12-26 6:00:00",

        "end of year": lambda year_time: f"{year_time}-12-31 23:59:59",

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
        "january": lambda year_time: f"{year_time}-01-01 0:00:00",
        "february": lambda year_time: f"{year_time}-02-01 0:00:00",
        "march": lambda year_time: f"{year_time}-03-01 0:00:00",
        "april": lambda year_time: f"{year_time}-04-01 0:00:00",
        "may": lambda year_time: f"{year_time}-05-01 0:00:00",
        "june": lambda year_time: f"{year_time}-06-01 0:00:00",
        "july": lambda year_time: f"{year_time}-07-01 0:00:00",
        "august": lambda year_time: f"{year_time}-08-01 0:00:00",
        "september": lambda year_time: f"{year_time}-09-01 0:00:00",
        "october": lambda year_time: f"{year_time}-10-01 0:00:00",
        "november": lambda year_time: f"{year_time}-11-01 0:00:00",
        "december": lambda year_time: f"{year_time}-12-01 0:00:00"
    }

    def __init__(self, parsed_object: list):
        self.parsed_object = parsed_object

    def evaluate(self) -> Union[datetime, None]:
        out = ""

        if self.parsed_object[0] == Method.ABSOLUTE_DATE_FORMATS:

            if len(self.parsed_object[1]) == 2:
                for object_type in self.parsed_object[1]:
                    if isinstance(object_type, AbsoluteDateTime):
                        out += f"{object_type.year}-{object_type.month}-{object_type.day} "

                    if isinstance(object_type, AbsoluteClockTime):
                        out += f"{object_type.hour}:{object_type.minute}:{object_type.second}"
            else:
                if isinstance(self.parsed_object[1][0], AbsoluteDateTime):
                    out += f"{self.parsed_object[1][0].year}-{self.parsed_object[1][0].month}-{self.parsed_object[1][0].day} 0:00:00"
                if isinstance(self.parsed_object[1][0], AbsoluteClockTime):
                    out += f"{datetime.strftime(self.CURRENT_DATE, '%Y-%m-%d')} {self.parsed_object[1][0].hour}:{self.parsed_object[1][0].minute}:{self.parsed_object[1][0].second}"

        if self.parsed_object[0] == Method.ABSOLUTE_PREPOSITIONS:
            pass

        if self.parsed_object[0] == Method.CONSTANTS:

            if len(self.parsed_object[1]) == 2:
                for object_type in self.parsed_object[1]:
                    if isinstance(object_type, Constant):
                        dt = datetime.strptime(f"{self.EVENTS[str(object_type.name)](self.parsed_object[1][1].year)}", "%Y-%m-%d %H:%M:%S")
                        if self.CURRENT_DATETIME > dt and self.parsed_object[1][1].year == 0:
                            dt += relativedelta(years=1)
                            out += f"{dt}"
                        else:
                            out += f"{dt}"

            else:
                if self.parsed_object[1][0].name in self.EVENTS:
                    if self.parsed_object[1][0].name == "infinity":
                        return self.EVENTS["infinity"]
                    dt = datetime.strptime(f"{self.EVENTS[str(self.parsed_object[1][0].name)](datetime.strftime(datetime.today(), '%Y'))}", "%Y-%m-%d %H:%M:%S")
                    if self.CURRENT_DATETIME > dt:
                        dt += relativedelta(years=1)
                        out += f"{dt}"
                    else:
                        out += f"{dt}"
                elif self.parsed_object[1][0].name in self.DAYS:
                    out += f"{self.DAYS[str(self.parsed_object[1][0].name)]}"

        if self.parsed_object[0] == Method.RELATIVE_DATETIMES:

            new = self.CURRENT_DATETIME

            new += relativedelta(
                years=self.parsed_object[1][0].years,
                months=self.parsed_object[1][0].months,
                weeks=self.parsed_object[1][0].weeks,
                days=self.parsed_object[1][0].days,
                hours=self.parsed_object[1][1].hours,
                minutes=self.parsed_object[1][1].minutes,
                seconds=self.parsed_object[1][1].seconds
            )

            out += f"{datetime.strftime(new, '%Y-%m-%d %H:%M:%S')}"

        if out:
            try:
                dt_object = datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
                return dt_object
            except ValueError:
                return None
