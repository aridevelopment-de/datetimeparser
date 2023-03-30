from typing import Any, Tuple, Union
from zoneinfo import ZoneInfo

from datetimeparser.utils.baseclasses import *
from datetimeparser.utils.enums import *
from datetimeparser.utils.exceptions import InvalidValue


class EvaluatorUtils:
    """
    Utils for the EvaluatorMethods-Class.
    """

    @staticmethod
    def get_week_of(dt: datetime) -> datetime:
        """
        Returns the first monday after a given date
        :param dt: datetime
        :return: datetime
        """

        return dt + timedelta(days=(7 - dt.weekday()))

    @staticmethod
    def x_week_of_month(relative_dt: RelativeDateTime, idx: int, parsed: List[Union[Any]], year):

        parsed[idx + 1] = EvaluatorUtils.datetime_to_absolute_datetime(parsed[idx + 1].time_value(year))

        relative_dt.days = EvaluatorUtils.get_week_of(
            EvaluatorUtils.absolute_datetime_to_datetime(parsed[idx + 1])
        ).day - 1

        relative_dt.weeks -= 1

        return parsed

    @staticmethod
    def absolute_datetime_to_datetime(absolute_datetime: AbsoluteDateTime) -> datetime:
        """
        Transforms an AbsoluteDateTime-object into a datetime-object
        :param absolute_datetime: the absolute_datetime-object
        :return: datetime
        """

        dt: datetime = datetime(
            year=absolute_datetime.year,
            month=absolute_datetime.month if absolute_datetime.month != 0 else 1,
            day=absolute_datetime.day if absolute_datetime.day != 0 else 1,
            hour=absolute_datetime.hour,
            minute=absolute_datetime.minute,
            second=absolute_datetime.second
        )

        return dt

    @staticmethod
    def datetime_to_absolute_datetime(dt: datetime) -> AbsoluteDateTime:
        """
        Transforms a datetime-object into an AbsoluteDateTime-object
        :param dt: the datetime
        :return: AbsoluteDateTime
        """

        absdt: AbsoluteDateTime = AbsoluteDateTime(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second
        )

        return absdt

    @staticmethod
    def sanitize_input(
            current_time: datetime, parsed_list: list
    ) -> Tuple[List[Union[RelativeDateTime, AbsoluteDateTime, int, Constant]], int]:
        """
        Removes useless keywords
        :param parsed_list: The list that should be sanitized
        :param current_time: The current time
        :return: a list without keywords
        """

        given_year = 0
        for idx, element in enumerate(parsed_list):
            if isinstance(element, Constant) and element.name == "of":
                if isinstance(parsed_list[idx - 1], RelativeDateTime):
                    relative_dt = parsed_list[idx - 1]
                    if relative_dt.years != 0:
                        relative_dt.years -= 1

                    if relative_dt.months != 0:
                        relative_dt.months -= 1

                    if relative_dt.weeks != 0:
                        if parsed_list[idx + 1] in MonthConstants.ALL:
                            try:
                                year = parsed_list.pop(idx + 2).year
                                given_year = year
                            except IndexError:
                                year = current_time.year

                            pars1, pars2 = parsed_list.copy(), parsed_list.copy()
                            ghost_parsed_list = EvaluatorUtils.x_week_of_month(relative_dt, idx, pars1, year)
                            test_out = EvaluatorUtils.add_relative_delta(
                                EvaluatorUtils.absolute_datetime_to_datetime(ghost_parsed_list[-1]),
                                ghost_parsed_list[0],
                                current_time
                            )
                            if current_time > test_out and not given_year:
                                parsed_list = EvaluatorUtils.x_week_of_month(relative_dt, idx, pars2, year + 1)

                else:
                    if isinstance(parsed_list[idx + 1], AbsoluteDateTime):
                        given_year = parsed_list[idx + 1].year

        return list(filter(lambda e: e not in Keywords.ALL and not isinstance(e, str), parsed_list)), given_year

    @staticmethod
    def cut_time(time: datetime) -> datetime:
        """
        Removes the time, only returning the date
        :param time: Time with hours, minutes, seconds
        :return: datetime
        """

        return datetime(time.year, time.month, time.day, 0, 0, 0)

    def get_base(self, sanitized_input: list, year: int, current_time: datetime, forced: bool = False) -> datetime:
        """
        Takes the last elements from the list and tries to generate a basis for further processing from them
        The base consists of at least one constant, to which values are then assigned
        :param sanitized_input: The sanitized list
        :param year: The year for the Constant
        :param current_time: The current datetime
        :param forced: If a given year should be used regardless of current time
        :return: datetime
        """

        # If a list contains an AbsoluteDateTime object that give more information about the time
        if isinstance(sanitized_input[-1], AbsoluteDateTime):
            # The Constant that the AbsoluteDateTime object should be based on (the year)
            if isinstance(sanitized_input[-2], Constant):
                # An Integer giving the information about the 'x'th of something (f.e. "first of august")
                if isinstance(sanitized_input[-3], int):
                    dt: datetime = sanitized_input[-2].time_value(sanitized_input[-1].year)
                    day: int = sanitized_input[-3]
                    return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)

                if sanitized_input[-2].time_value:
                    dt = sanitized_input[-2].time_value(sanitized_input[-1].year)

                    if isinstance(sanitized_input[-3], Constant) and sanitized_input[-3].value:
                        dt += relativedelta(days=sanitized_input[-3].value - 1)
                    elif isinstance(sanitized_input[-3], Constant) and not sanitized_input[-3].value:
                        val = sanitized_input[-4].value

                        if sanitized_input[-3].name == "days":
                            return datetime(dt.year, dt.month, val, dt.hour, dt.minute, dt.second)
                        if sanitized_input[-3].name == "weeks":
                            dt = self.get_week_of(dt)
                            return dt + relativedelta(weeks=val-1)
                        if sanitized_input[-3].name == "months":
                            return datetime(dt.year, val, dt.day, dt.hour, dt.minute, dt.second)

                        days_dict = {x.name: x.time_value(dt) for x in WeekdayConstants.ALL}
                        if sanitized_input[-3].name in days_dict:
                            dt = datetime.strptime(days_dict.get(sanitized_input[-3].name), "%Y-%m-%d %H:%M:%S")
                            dt += relativedelta(weeks=val - 1)

                    return dt

                else:
                    if sanitized_input[-3].value:
                        val: int = sanitized_input[-3].value

                        if sanitized_input[-2].name == "days":
                            return datetime(sanitized_input[-1].year, 1, val, 0, 0, 0)
                        if sanitized_input[-2].name == "months":
                            return datetime(sanitized_input[-1].year, val, 1, 0, 0, 0)

            # If a year is given but no months/days, they will be set to '1' because datetime can't handle month/day-values with '0'
            if sanitized_input[-1].year != 0:
                year = sanitized_input[-1].year
                month = sanitized_input[-1].month if sanitized_input[-1].month != 0 else 1
                day = sanitized_input[-1].day if sanitized_input[-1].day != 0 else 1

                return datetime(year, month, day)

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

        # If no AbsoluteDatetime is given, the default year will be used instead
        elif isinstance(sanitized_input[-1], Constant):
            dt: datetime = sanitized_input[-1].time_value(year)
            if isinstance(sanitized_input[-2], int):
                day: int = sanitized_input[-2]
                out = datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)

                if out > current_time or forced:
                    return out
                out += relativedelta(years=1)
                return out
            else:
                if len(sanitized_input) == 3:
                    val: int = sanitized_input[-3].value

                    if sanitized_input[-2].name == "days":
                        return datetime(dt.year, dt.month, dt.day + val, dt.hour, dt.minute, dt.second)
                    if sanitized_input[-2].name == "weeks":
                        dt = self.get_week_of(dt)
                        return dt + relativedelta(weeks=val)
                    if sanitized_input[-2].name == "months":
                        return datetime(dt.year, dt.month + val, dt.day, dt.hour, dt.minute, dt.second)
                if not isinstance(sanitized_input[-2], RelativeDateTime):
                    return datetime(dt.year, dt.month, sanitized_input[-2].value, dt.hour, dt.minute, dt.second)

            # Checks if an event already happened this year (f.e. eastern). If so, the next year will be used
            if sanitized_input[-1].time_value(year) > current_time or forced:
                return sanitized_input[-1].time_value(year)
            else:
                return sanitized_input[-1].time_value(year + 1)

    @staticmethod
    def calc_relative_time(sanitized_list: list) -> RelativeDateTime:
        """
        Adds all RelativeDateTime-objects in a list together in one single object
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
    def add_relative_delta(base_time: datetime, rel_time: RelativeDateTime, current_time: datetime) -> datetime:
        """
        Prepares a RelativeDateTime-object for adding to a datetime
        :param base_time: DateTime-object the time should be added too
        :param rel_time: RelativeDateTime-object
        :param current_time: current datetime
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

        try:
            if base_time > current_time > base_time + rel:
                rel.years += 1
            out = base_time + rel
        except ValueError as e:
            raise InvalidValue(e.args[0])

        return out

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

    @staticmethod
    def daylight_saving(tz: str):
        """checks if a timezone currently saves daylight (winter-/summer-time)"""
        return bool(datetime.now(ZoneInfo(tz)).dst())
