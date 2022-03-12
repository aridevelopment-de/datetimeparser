from typing import Union

from .baseclasses import *
from .enums import *


class AbsolutePrepositionsEvaluator:

    @staticmethod
    def sanitize_input(parsed_list: list) -> list:
        """removes useless keywords"""
        return [element for element in parsed_list if element not in Keywords.ALL]

    @staticmethod
    def get_base(sanitized_input: list, year: int) -> datetime:
        if isinstance(sanitized_input[-1], AbsoluteDateTime):
            if isinstance(sanitized_input[-2], Constant):
                if isinstance(sanitized_input[-3], int):
                    dt: datetime = sanitized_input[-2].time_value(sanitized_input[-1].year)
                    day: int = sanitized_input[-3]
                    return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)
                return sanitized_input[-2].time_value(sanitized_input[-1].year)
            return datetime(sanitized_input[-1].year, 1, 1)
        elif isinstance(sanitized_input[-1], Constant):
            if isinstance(sanitized_input[-2], int):
                dt: datetime = sanitized_input[-1].time_value(year)
                day: int = sanitized_input[-2]
                return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)
            return sanitized_input[-1].time_value(year)

    @staticmethod
    def calc_relative_time(sanitized_list: list) -> RelativeDateTime:
        rel_list = [relative_time for relative_time in sanitized_list if isinstance(relative_time, RelativeDateTime)]

        ev_out = RelativeDateTime()
        for i in rel_list:
            ev_out.years += i.years
            ev_out.months += i.months
            ev_out.weeks += i.weeks
            ev_out.days += i.days
            ev_out.hours += i.hours
            ev_out.minutes += i.minutes
            ev_out.seconds += i.seconds

        return ev_out


def evaluate_absolute_date_formats(current_time: datetime, parsed: AbsoluteDateTime) -> AbsoluteDateTime:
    ev_out = AbsoluteDateTime(
        year=current_time.year if parsed.year == 0 else parsed.year,
        month=current_time.month if parsed.month == 0 else parsed.month,
        day=current_time.day if parsed.day == 0 else parsed.day,
        hour=parsed.hour,
        minute=parsed.minute,
        second=parsed.second
    )

    return ev_out


def evaluate_absolute_prepositions(current_time: datetime, parsed: list):  # -> AbsoluteDateTime:
    ev = AbsolutePrepositionsEvaluator()
    base_year = current_time.year
    sanitized = ev.sanitize_input(parsed)
    base = ev.get_base(sanitized, base_year)
    rel_out = ev.calc_relative_time(sanitized)

    base += relativedelta(
        years=rel_out.years,
        months=rel_out.months,
        weeks=rel_out.weeks,
        days=rel_out.days,
        hours=rel_out.hours,
        minutes=rel_out.minutes,
        seconds=rel_out.seconds
    )

    return base


def evaluate_constants(current_time: datetime, parsed_object) -> Union[AbsoluteDateTime, datetime, int]:
    print(parsed_object)
    dt: datetime = current_time
    object_type: Constant = parsed_object[0]

    if len(parsed_object) == 2:
        if isinstance(parsed_object[0], Constant):
            object_year: AbsoluteDateTime = parsed_object[1].year
            dt = object_type.time_value(object_year)

            if current_time > dt and object_year == 0:
                dt += relativedelta(years=1)

    else:
        if object_type.name == "infinity":
            return object_type.value

        elif object_type in WeekdayConstants.ALL:
            dt: datetime = datetime.strptime(
                object_type.time_value(current_time),
                "%Y-%m-%d %H:%M:%S"
            )

        else:
            dt = object_type.time_value(current_time.year)

        if current_time > dt and parsed_object[0] not in Constants.ALL_RELATIVE_CONSTANTS:
            dt += relativedelta(years=1)

    ev_out = AbsoluteDateTime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )

    return ev_out


def evaluate_relative_datetimes(current_time: datetime, parsed: RelativeDateTime) -> AbsoluteDateTime:
    out: datetime = current_time

    out += relativedelta(
        years=parsed.years,
        months=parsed.months,
        weeks=parsed.weeks,
        days=parsed.days,
        hours=parsed.hours,
        minutes=parsed.minutes,
        seconds=parsed.seconds
    )

    ev_out = AbsoluteDateTime(
        out.year, out.month, out.day, out.hour, out.minute, out.second
    )

    return ev_out


def evaluate_datetime_delta_constants(current_time: datetime, parsed: RelativeDateTime) -> AbsoluteDateTime:
    ev_out = AbsoluteDateTime(
        current_time.year, current_time.month, current_time.day, parsed.hours, parsed.minutes, parsed.seconds
    )

    return ev_out
