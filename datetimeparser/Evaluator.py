from datetime import datetime, timedelta

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

curent_date = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d")
curent_datetime = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

class Evaluator:
    EVENTS = {
        "silvester": lambda year: f"{year}-12-31 0:00:00",
        "nicholas": lambda year: f"{year}-12-06 0:00:00",
        "christmas": lambda year: f"{year}-12-25 0:00:00",
        "halloween": lambda year: f"{year}-10-31 0:00:00",
    }

    DAYS = {
        "monday": f"{curent_date + timedelta((0-curent_date.weekday())%7)}",
        "tuesday": f"{curent_date + timedelta((1-curent_date.weekday())%7)}",
        "wednesday": f"{curent_date + timedelta((2-curent_date.weekday())%7)}",
        "thursday": f"{curent_date + timedelta((3-curent_date.weekday())%7)}",
        "friday": f"{curent_date + timedelta((4-curent_date.weekday())%7)}",
        "saturday": f"{curent_date + timedelta((5-curent_date.weekday())%7)}",
        "sunday": f"{curent_date + timedelta((6-curent_date.weekday())%7)}"
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
                    out += f"{datetime.strftime(curent_date, '%Y-%m-%d')} {self.parsed_object[1][0].hour}:{self.parsed_object[1][0].minute}:{self.parsed_object[1][0].second}"
        

        if self.parsed_object[0] == Method.ABSOLUTE_PREPOSITIONS:
            pass


        if self.parsed_object[0] == Method.CONSTANTS:

            if len(self.parsed_object[1]) == 2:
                for object_type in self.parsed_object[1]:
                    if isinstance(object_type, Constant):
                        if str(object_type.name) == "eastern":
                            out = f"{eastern_calc(self.parsed_object[1][1].year)}"
                        else:
                            out += f"{self.EVENTS[str(object_type.name)](self.parsed_object[1][1].year)}"

            else:
                if self.parsed_object[1][0].name in self.EVENTS:
                    out += f"{self.EVENTS[str(self.parsed_object[1][0].name)](datetime.strftime(datetime.today(), '%Y'))}"
                else:
                    out += f"{self.DAYS[str(self.parsed_object[1][0].name)]}"


        if self.parsed_object[0] == Method.RELATIVE_DATETIMES:
            pass


        if out:
            try:
                dt_object = datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
                return dt_object
            except ValueError:
                return None
