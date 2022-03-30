from .baseclasses import *
from .enums import *


class EvaluatorUtils:
    """
    Utils for the EvaluatorMethods-Class.
    """

    @staticmethod
    def sanitize_input(parsed_list: list) -> list:
        """
        Removes useless keywords.

        :param parsed_list: The list that should be sanitized
        :return: list
        """

        return [element for element in parsed_list if element not in Keywords.ALL and not isinstance(element, str)]

    @staticmethod
    def cut_time(time: datetime) -> datetime:
        """
        Removes the time, only returning the date

        :param time: Time with hours, minutes, seconds
        :return: datetime
        """

        return datetime(time.year, time.month, time.day, 0, 0, 0)

    @staticmethod
    def get_base(sanitized_input: list, year: int, current_time: datetime) -> datetime:
        """
        Takes the last elements from the list and tries to generate a basis for further processing from them.
        The base consists of at least one constant, to which values are then assigned.

        :param sanitized_input: The sanitized list
        :param year: The year for the Constant
        :param current_time: The current datetime
        :return: datetime
        """

        if isinstance(sanitized_input[-1], AbsoluteDateTime):
            if isinstance(sanitized_input[-2], Constant):
                if isinstance(sanitized_input[-3], int):
                    dt: datetime = sanitized_input[-2].time_value(sanitized_input[-1].year)
                    day: int = sanitized_input[-3]
                    return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)
                return sanitized_input[-2].time_value(sanitized_input[-1].year)
            if sanitized_input[-1].year != 0:
                return datetime(sanitized_input[-1].year, 1, 1)
            else:
                dt = datetime(
                    year=current_time.year if sanitized_input[-1].year == 0 else sanitized_input[-1].year,
                    month=current_time.month if sanitized_input[-1].month == 0 else sanitized_input[-1].month,
                    day=current_time.day if sanitized_input[-1].day == 0 else sanitized_input[-1].day,
                    hour=sanitized_input[-1].hour,
                    minute=sanitized_input[-1].minute,
                    second=sanitized_input[-1].second
                )
                return dt
        elif isinstance(sanitized_input[-1], Constant):
            if isinstance(sanitized_input[-2], int):
                dt: datetime = sanitized_input[-1].time_value(year)
                day: int = sanitized_input[-2]
                return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)
            return sanitized_input[-1].time_value(year)

    @staticmethod
    def calc_relative_time(sanitized_list: list) -> RelativeDateTime:
        """
        Adds all RelativeDateTime-objects in a list together in one single object.

        :param sanitized_list: The sanitized list
        :return: RelativeDateTime
        """

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
    def prepare_relative_delta(rel_time: RelativeDateTime) -> relativedelta:
        """
        Prepares a RelativeDateTime-object for adding to a datetime.

        :param rel_time: RelativeDateTime-object
        :return: relativedelta
        """

        rel = relativedelta(
            years=rel_time.years,
            months=rel_time.months,
            weeks=rel_time.weeks,
            days=rel_time.days,
            hours=rel_time.hours,
            minutes=rel_time.minutes,
            seconds=rel_time.seconds
        )

        return rel

    @staticmethod
    def remove_milli_seconds(dt: datetime) -> datetime:
        """
        Cuts milliseconds of.

        :param dt: The time with milliseconds at the end
        :return: datetime
        """

        return datetime.strptime(dt.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_offset(con: Constant, offset) -> RelativeDateTime:
        """
        Calculates the UTC-offset from a Constant-object

        :param con: the Constant
        :param offset: the UTC-offset from the timezone
        :return: RelativeDateTime
        """

        off: int = 0
        if con.offset:
            if con.offset < 0:
                off += abs(con.offset)
            else:
                off += con.offset

            return RelativeDateTime(hours=off + offset.seconds / 3600 + offset.days * 24)


class EvaluatorMethods(EvaluatorUtils):
    """
    Evaluates a datetime-object from a given list returned from the parser
    """

    def __init__(self, parsed, current_time: datetime, offset: timedelta = None):
        """
        :param parsed: object returned from the parser
        :param current_time: the current datetime
        :param offset: the UTC-offset from the current timezone. Default: None
        """

        self.parsed = parsed
        self.current_time = current_time
        self.offset = offset

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
        sanitized = self.sanitize_input(self.parsed)
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
            base += self.prepare_relative_delta(sanitized[-1])

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
        sanitized = self.sanitize_input(self.parsed)
        base = self.get_base(sanitized, base_year, self.current_time)
        rel_out = self.calc_relative_time(sanitized)
        base += self.prepare_relative_delta(rel_out)

        return self.remove_milli_seconds(base)

    def evaluate_constants(self) -> datetime:
        dt: datetime = self.current_time
        object_type: Constant = self.parsed[0]

        if len(self.parsed) == 2:
            if isinstance(self.parsed[0], Constant):
                object_year: AbsoluteDateTime = self.parsed[1].year
                dt = object_type.time_value(object_year)

                if self.current_time > dt and object_year == 0:
                    dt += relativedelta(years=1)

        else:
            if object_type.name == "infinity":
                raise ValueError("'infinity' isn't a valid time")

            elif object_type in WeekdayConstants.ALL:
                dt: datetime = datetime.strptime(
                    object_type.time_value(self.cut_time(self.current_time)),
                    "%Y-%m-%d %H:%M:%S"
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

            if self.current_time > dt and self.parsed[0] not in Constants.ALL_RELATIVE_CONSTANTS:
                dt += relativedelta(years=1)

        ev_out = datetime(
            dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
        )

        if object_type.offset:
            ev_out += self.prepare_relative_delta(self.get_offset(object_type, self.offset))

        return ev_out

    def evaluate_relative_datetime(self) -> datetime:
        out: datetime = self.current_time

        out += self.prepare_relative_delta(self.parsed)
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
