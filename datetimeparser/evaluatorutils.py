from typing import Union

from .baseclasses import *
from .enums import *


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
    def sanitize_input(current_time: datetime, parsed_list: list) -> list[Union[RelativeDateTime, AbsoluteDateTime, int, Constant]]:
        """
        Removes useless keywords
        :param parsed_list: The list that should be sanitized
        :param current_time: The current time
        :return: a list without keywords
        """

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
                            except IndexError:
                                year = current_time.year
                            parsed_list[idx + 1] = EvaluatorUtils.datetime_to_absolute_datetime(parsed_list[idx + 1].time_value(year))

                        relative_dt.days = EvaluatorUtils.get_week_of(
                                                EvaluatorUtils.absolute_datetime_to_datetime(parsed_list[idx + 1])
                                            ).day - 1

                        relative_dt.weeks -= 1

        return list(filter(lambda e: e not in Keywords.ALL and not isinstance(e, str), parsed_list))

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
        Takes the last elements from the list and tries to generate a basis for further processing from them
        The base consists of at least one constant, to which values are then assigned
        :param sanitized_input: The sanitized list
        :param year: The year for the Constant
        :param current_time: The current datetime
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
                return sanitized_input[-2].time_value(sanitized_input[-1].year)

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
            if isinstance(sanitized_input[-2], int):
                dt: datetime = sanitized_input[-1].time_value(year)
                day: int = sanitized_input[-2]

                return datetime(dt.year, dt.month, day, dt.hour, dt.minute, dt.second)

            # Checks if an event already happened this year (f.e. eastern). If so, the next year will be used
            if sanitized_input[-1].time_value(year) > current_time:
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
    def prepare_relative_delta(rel_time: RelativeDateTime) -> relativedelta:
        """
        Prepares a RelativeDateTime-object for adding to a datetime
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
        Cuts milliseconds of
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
