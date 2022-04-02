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
        for index, element in enumerate(parsed_list):
            if isinstance(element, Constant) and element.name == "of":
                if isinstance(parsed_list[index - 1], RelativeDateTime):
                    if parsed_list[index - 1].years != 0:
                        parsed_list[index - 1].years -= 1
                    if parsed_list[index - 1].months != 0:
                        parsed_list[index - 1].months -= 1

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
