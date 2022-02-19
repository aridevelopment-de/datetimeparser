from dateutil.relativedelta import relativedelta
from typing import Union

from .baseclasses import *
from .enums import *


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

        if current_time > dt:
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
