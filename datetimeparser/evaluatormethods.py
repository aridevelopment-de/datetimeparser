from typing import Union

from .baseclasses import *
from .enums import *


class AbsolutePrepositionsEvaluator:

    @staticmethod
    def sanitize_input(parsed_list: list) -> list:
        """removes useless keywords"""
        return [element for element in parsed_list if element not in Keywords.ALL and not isinstance(element, str)]

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

    @staticmethod
    def remove_milli_seconds(dt: datetime) -> datetime:
        return datetime.strptime(dt.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")


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


def evaluate_constant_relatives(current_time: datetime, parsed: list) -> datetime:
    sanitized = AbsolutePrepositionsEvaluator.sanitize_input(parsed)
    base: datetime = current_time
    ev_out = None

    if isinstance(sanitized[-1], Constant):
        base = sanitized[-1].time_value(current_time.year)
        hour, minute, sec = sanitized[-2].time_value(None)
        ev_out = datetime(base.year, base.month, base.day, hour, minute, sec)

    elif isinstance(sanitized[-1], RelativeDateTime):
        base += relativedelta(
            years=sanitized[-1].years,
            months=sanitized[-1].months,
            weeks=sanitized[-1].weeks,
            days=sanitized[-1].days,
            hours=sanitized[-1].hours,
            minutes=sanitized[-1].minutes,
            seconds=sanitized[-1].seconds
        )
        if sanitized[-2] in WeekdayConstants.ALL:
            ev_out = datetime.strptime(
                sanitized[-2].time_value(base),
                "%Y-%m-%d %H:%M:%S"
            )
        elif sanitized[-2] in Constants.ALL_RELATIVE_CONSTANTS:
            base = sanitized[-2].time_value(None)
            hour, minute, sec = sanitized[-1].hours, sanitized[-1].minutes, sanitized[-1].seconds
            ev_out = datetime(base.year, base.month, base.day, hour, minute, sec)

        elif sanitized[-2] in DatetimeDeltaConstants.ALL:
            ev_out = datetime(
                year=base.year,
                month=base.month,
                day=base.day,
                hour=sanitized[-2].time_value(None)[0],
                minute=sanitized[-2].time_value(None)[1],
                second=sanitized[-2].time_value(None)[2]
            )

    elif isinstance(sanitized[-1], AbsoluteDateTime):
        base = datetime(
            year=current_time.year if sanitized[-1].year == 0 else sanitized[-1].year,
            month=current_time.month if sanitized[-1].month == 0 else sanitized[-1].month,
            day=current_time.day if sanitized[-1].day == 0 else sanitized[-1].day,
            hour=sanitized[-1].hour,
            minute=sanitized[-1].minute,
            second=sanitized[-1].second
        )
        hour, minute, sec = sanitized[-2].time_value(None)
        ev_out = datetime(base.year, base.month, base.day, hour, minute, sec)

    return ev_out


def evaluate_absolute_prepositions(current_time: datetime, parsed: list) -> datetime:
    ev = AbsolutePrepositionsEvaluator
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

    return ev.remove_milli_seconds(base)


def evaluate_constants(current_time: datetime, parsed_object) -> Union[AbsoluteDateTime, datetime, int]:
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

            if isinstance(dt, tuple):
                dt = datetime(
                    year=current_time.year,
                    month=current_time.month,
                    day=current_time.day,
                    hour=dt[0],
                    minute=dt[1],
                    second=dt[2]
                )

        if current_time > dt and parsed_object[0] not in Constants.ALL_RELATIVE_CONSTANTS:
            dt += relativedelta(years=1)

    ev_out = AbsoluteDateTime(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )

    return ev_out


def evaluate_relative_datetime(current_time: datetime, parsed: RelativeDateTime) -> AbsoluteDateTime:
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
