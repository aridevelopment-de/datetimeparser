from typing import Any, Optional, Tuple

from datetimeparser.evaluator.evaluatorutils import EvaluatorUtils
from datetimeparser.utils.baseclasses import *
from datetimeparser.utils.enums import *
from datetimeparser.utils.exceptions import InvalidValue
from datetimeparser.utils.formulars import calc_sun_time
from datetimeparser.utils.geometry import TimeZoneManager


class EvaluatorMethods(EvaluatorUtils):
    """
    Evaluates a datetime-object from a given list returned from the parser
    """

    def __init__(
            self, parsed: Any, current_time: datetime, timezone: str, coordinates: Optional[Tuple[float, float]], offset: timedelta = None
    ):
        """
        :param parsed: object returned from the parser
        :param current_time: the current datetime
        :param timezone: the given timezone
        :param coordinates: coordinates from the timezone
        :param offset: the UTC-offset from the current timezone. Default: None
        """

        self.parsed = parsed
        self.current_time = current_time
        self.offset = offset
        self.coordinates = coordinates
        self.timezone = timezone

    def evaluate_absolute_date_formats(self) -> datetime:
        ev_out = datetime(
            year=self.current_time.year if self.parsed.year == 0 else self.parsed.year,
            month=self.current_time.month if self.parsed.month == 0 else self.parsed.month,
            day=self.current_time.day if self.parsed.day == 0 else self.parsed.day,
            hour=self.parsed.hour,
            minute=self.parsed.minute,
            second=self.parsed.second
        )

        return ev_out

    def evaluate_constant_relatives(self) -> datetime:
        sanitized, _ = self.sanitize_input(self.current_time, self.parsed)
        base: datetime = self.current_time
        ev_out = None

        if isinstance(sanitized[-1], Constant):
            base = sanitized[-1].time_value(self.current_time.year)
            if isinstance(sanitized[-2], Constant):
                hour, minute, sec = sanitized[-2].time_value(None)
            else:
                hour, minute, sec = sanitized[-2].hour, sanitized[-2].minute, sanitized[-2].second
            ev_out = datetime(base.year, base.month, base.day, hour, minute, sec)

        elif isinstance(sanitized[-1], RelativeDateTime):
            base = self.add_relative_delta(base, sanitized[-1], self.current_time)

            if sanitized[-2] in WeekdayConstants.ALL:
                base = self.cut_time(base)
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

            elif sanitized[-2] in Constants.ALL:
                ev_out = sanitized[-2].time_value(base.year)

        elif isinstance(sanitized[-1], AbsoluteDateTime):
            base = datetime(
                year=self.current_time.year if sanitized[-1].year == 0 else sanitized[-1].year,
                month=self.current_time.month if sanitized[-1].month == 0 else sanitized[-1].month,
                day=self.current_time.day if sanitized[-1].day == 0 else sanitized[-1].day,
                hour=sanitized[-1].hour,
                minute=sanitized[-1].minute,
                second=sanitized[-1].second
            )

            hour, minute, sec = sanitized[-2].time_value(None)
            ev_out = datetime(base.year, base.month, base.day, hour, minute, sec)

        return ev_out

    def evaluate_absolute_prepositions(self) -> datetime:
        base_year = self.current_time.year
        sanitized, given_year = self.sanitize_input(self.current_time, self.parsed)
        if not given_year:
            base = self.get_base(sanitized, base_year, self.current_time)
        else:
            base = self.get_base(sanitized, given_year, self.current_time, forced=True)
        rel_out = self.calc_relative_time(sanitized)
        base = self.add_relative_delta(base, rel_out, self.current_time)

        return base

    def evaluate_constants(self) -> Tuple[datetime, Optional[Tuple[float, float]]]:
        dt: datetime = self.current_time
        object_type: Constant = self.parsed[0]

        if len(self.parsed) == 2:
            if isinstance(self.parsed[0], Constant):
                object_year: int = self.parsed[1].year
                dt = object_type.time_value(object_year)

                if self.current_time > dt and object_year == 0:
                    dt = object_type.time_value(object_year + 1)

        else:
            if object_type.name == "infinity":  # TODO: has to be improved for more invalid constants if needed
                raise InvalidValue(object_type.name)

            elif object_type in WeekdayConstants.ALL:
                dt: datetime = datetime.strptime(
                    object_type.time_value(self.cut_time(self.current_time)),
                    "%Y-%m-%d %H:%M:%S"
                )

            elif object_type.name == "sunset" or object_type.name == "sunrise":
                ofs = self.offset.total_seconds() / 60 / 60  # -> to hours
                # TODO: at the moment summer and winter time change the result for the offset around 1 hour
                if not self.coordinates:
                    self.coordinates = TimeZoneManager().get_coordinates(self.timezone)

                dt = calc_sun_time(
                    self.current_time,
                    (self.coordinates[0], self.coordinates[1], ofs),
                    object_type.name == "sunrise"
                )

            else:
                dt = object_type.time_value(self.current_time.year)
                if isinstance(dt, tuple):
                    dt = datetime(
                        year=self.current_time.year,
                        month=self.current_time.month,
                        day=self.current_time.day,
                        hour=dt[0],
                        minute=dt[1],
                        second=dt[2]
                    )
                    return dt, self.coordinates

            if self.current_time >= dt and self.parsed[0] not in (
                    Constants.ALL_RELATIVE_CONSTANTS and WeekdayConstants.ALL and DatetimeDeltaConstants.CHANGING
            ):
                dt = object_type.time_value(self.current_time.year + 1)

            if self.current_time >= dt and self.parsed[0] in WeekdayConstants.ALL:
                dt += relativedelta(days=7)

        ev_out = datetime(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )

        if object_type.offset:
            ev_out = self.add_relative_delta(ev_out, self.get_offset(object_type, self.offset), self.current_time)
            if self.daylight_saving(self.timezone):
                ev_out -= timedelta(hours=1)

        return ev_out, self.coordinates

    def evaluate_relative_datetime(self) -> datetime:
        out: datetime = self.current_time

        out = self.add_relative_delta(out, self.parsed, self.current_time)
        ev_out = datetime(
            out.year, out.month, out.day, out.hour, out.minute, out.second
        )

        return ev_out

    def evaluate_datetime_delta_constants(self) -> datetime:
        ev_out = datetime(
            self.current_time.year, self.current_time.month, self.current_time.day,
            self.parsed.hour, self.parsed.minute, self.parsed.second
        )

        return ev_out
