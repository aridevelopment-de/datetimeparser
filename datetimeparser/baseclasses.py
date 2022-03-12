from __future__ import annotations  # noqa: I2041

from typing import Callable, List, TYPE_CHECKING

if TYPE_CHECKING:
    from datetimeparser.enums import ConstantOption  # noqa: I2041


class Printable:
    FIELDS = []

    def __str__(self):
        return f'<{str(self.__class__)[7:-1]} {" ".join("%s=%s" % (field, getattr(self, field)) for field in self.FIELDS if getattr(self, field) is not None)}>'

    def __repr__(self):
        return self.__str__()


class Concatenable(Printable):
    @classmethod
    def _concatenate(cls, new, o1, o2):
        for field in cls.FIELDS:
            d1 = getattr(o1, field)
            d2 = getattr(o2, field)

            if d1 == 0 and d2 == 0:
                continue

            if d1 != 0 and d2 != 0:
                setattr(new, field, d2)

            if d1 == 0:
                setattr(new, field, d2)
            elif d2 == 0:
                setattr(new, field, d1)

        return new


class AbsoluteDateTime(Concatenable):
    FIELDS = ["year", "month", "day", "hour", "minute", "second"]

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    @classmethod
    def concatenate(cls, o1: 'AbsoluteDateTime', o2: 'AbsoluteDateTime') -> 'AbsoluteDateTime':
        return cls._concatenate(AbsoluteDateTime(), o1, o2)


class RelativeDateTime(Concatenable):
    FIELDS = ["years", "months", "weeks", "days", "hours", "minutes", "seconds"]

    def __init__(self, years=0, months=0, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def concatenate(cls, o1: 'RelativeDateTime', o2: 'RelativeDateTime') -> 'RelativeDateTime':
        return cls._concatenate(RelativeDateTime(), o1, o2)


class Constant(Printable):
    FIELDS = ["name", "alias", "value", "time_value"]

    def __init__(self, name, alias=None, value=None, options: List['ConstantOption'] = None, time_value: Callable = None):
        self.name = name
        self.alias = alias or []
        self.value = value
        self.options = options or []
        self.time_value = time_value

    def get_all(self):
        return [self.name, *self.alias]


class MethodEnum:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"<Method: {self.name}>"

    def __repr__(self):
        return f"<Method: {self.name}>"
