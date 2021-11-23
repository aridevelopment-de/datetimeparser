from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .baseclasses import *


def eastern_calc(year: int) -> str:
    A = year % 19
    K = year // 100
    M = 15 + (3*K+3) // 4 - (8*K+13) // 25
    D = (19*A+M) % 30
    S = 2 - (3*K+3) // 4
    R = D // 29 + (D//28-D//29) * (A//11)
    OG = 21 + D + R
    SZ = 7 - (year+year//4+S) % 7
    OE = 7 - (OG-SZ) % 7
    OS = OG + OE

    if OS > 32:
        return f"{year}-04-{OS-31} 0:00:00"
    else:
        return f"{year}-03-{OS} 0:00:00"


def thanksgiving_calc(year: int) -> str:
    YEAR = datetime.strptime(f"{year}-11-29 0:00:00", "%Y-%m-%d %H:%M:%S")
    DATE = datetime.strptime(f"{year}-11-3 0:00:00", "%Y-%m-%d %H:%M:%S")
    return YEAR - timedelta(days=(DATE.weekday() + 2))


def days_feb(year: int) -> str:
    if int(year) % 400 == 0 or int(year) % 4 == 0 and not int(year) % 100 == 0:
        return "29"
    else:
        return "28"


class Evaluator:
    CURENT_DATE = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d")
    CURENT_DATETIME = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    EVENTS = {
        "silvester": lambda year: f"{year}-12-31 0:00:00",
        "nicholas": lambda year: f"{year}-12-06 0:00:00",
        "christmas": lambda year: f"{year}-12-25 0:00:00",
        "halloween": lambda year: f"{year}-10-31 0:00:00",
        "april fools day": lambda year: f"{year}-04-01 0:00:00",
        "eastern": eastern_calc,
        "thanksgiving": thanksgiving_calc,
        "saint patrick's day": lambda year: f"{year}-03-17 0:00:00",
        "valentines day": lambda year: f"{year}-02-14 0:00:00",

        # metereological dates, if someone has any problem with that... -> fork this project, build a function for that and create a pull request :)
        "spring begin": lambda year: f"{year}-03-01 0:00:00",
        "spring end": lambda year: f"{year}-05-31 23:59:59",
        "summer begin": lambda year: f"{year}-06-01 0:00:00",
        "summer end": lambda year: f"{year}-08-31 23:59:59",
        "fall begin": lambda year: f"{year}-09-01 0:00:00",
        "fall end": lambda year: f"{year}-11-30 23:59:59",
        "winter begin": lambda year: f"{year}-12-01 0:00:00",
        "winter end": lambda year: f"{year}-02-{days_feb(year)} 23:59:59",

        "aoc begin": lambda year: f"{year}-12-01 6:00:00",
        "aoc end": lambda year: f"{year}-12-26 6:00:00",

        "end of year": lambda year: f"{year}-12-31 23:59:59",

        "infinity": -1
    }

    DAYS = {
        "monday": f"{CURENT_DATE + timedelta((0-CURENT_DATE.weekday())%7)}",
        "tuesday": f"{CURENT_DATE + timedelta((1-CURENT_DATE.weekday())%7)}",
        "wednesday": f"{CURENT_DATE + timedelta((2-CURENT_DATE.weekday())%7)}",
        "thursday": f"{CURENT_DATE + timedelta((3-CURENT_DATE.weekday())%7)}",
        "friday": f"{CURENT_DATE + timedelta((4-CURENT_DATE.weekday())%7)}",
        "saturday": f"{CURENT_DATE + timedelta((5-CURENT_DATE.weekday())%7)}",
        "sunday": f"{CURENT_DATE + timedelta((6-CURENT_DATE.weekday())%7)}"
    }


    def __init__(self, parsed_object: list):
        self.parsed_object = parsed_object


    def evaluate(self) -> datetime:
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
                    out += f"{datetime.strftime(self.CURENT_DATE, '%Y-%m-%d')} {self.parsed_object[1][0].hour}:{self.parsed_object[1][0].minute}:{self.parsed_object[1][0].second}"
        

        if self.parsed_object[0] == Method.ABSOLUTE_PREPOSITIONS:
            pass


        if self.parsed_object[0] == Method.CONSTANTS:

            if len(self.parsed_object[1]) == 2:
                for object_type in self.parsed_object[1]:
                    if isinstance(object_type, Constant):
                        dt = datetime.strptime(f"{self.EVENTS[str(object_type.name)](self.parsed_object[1][1].year)}", "%Y-%m-%d %H:%M:%S")
                        if self.CURENT_DATETIME > dt and self.parsed_object[1][1].year == 0:
                            dt += relativedelta(years=1)
                            out += f"{dt}"
                        else:
                            out += f"{dt}"

            else:
                if self.parsed_object[1][0].name in self.EVENTS:
                    if self.parsed_object[1][0].name == "infinity":
                            return self.EVENTS["infinity"]
                    dt = datetime.strptime(f"{self.EVENTS[str(self.parsed_object[1][0].name)](datetime.strftime(datetime.today(), '%Y'))}", "%Y-%m-%d %H:%M:%S")
                    if self.CURENT_DATETIME > dt:
                        dt += relativedelta(years=1)
                        out += f"{dt}"
                    else:
                        out += f"{dt}"
                else:
                    out += f"{self.DAYS[str(self.parsed_object[1][0].name)]}"


        if self.parsed_object[0] == Method.RELATIVE_DATETIMES:

            new = self.CURENT_DATETIME

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
