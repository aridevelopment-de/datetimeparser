class Printable:
    FIELDS = []

    def __str__(self):
        return f'<{str(self.__class__)[7:-1]} {" ".join("%s=%s" % (field, getattr(self, field)) for field in self.FIELDS if getattr(self, field) is not None)}>'

    def __repr__(self):
        return self.__str__()


class EvaluatorOutput(Printable):
    FIELDS = ["year", "month", "day", "hour", "minute", "second"]

    def __init__(self, year=0, month=0, day=0, hour=0, minute=0, second=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second


class AbsoluteDate(Printable):
    FIELDS = ["year", "month", "day"]

    def __init__(self, year=0, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day


class AbsoluteTime(Printable):
    FIELDS = ["hour", "minute", "second"]

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second


class RelativeDate(Printable):
    FIELDS = ["years", "months", "weeks", "days"]

    def __init__(self, years=0, months=0, weeks=0, days=0):
        self.years = years
        self.months = months
        self.weeks = weeks
        self.days = days

    @classmethod
    def concatenate(cls, o1: 'RelativeDate', o2: 'RelativeDate') -> 'RelativeDate':
        new = RelativeDate()

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


class RelativeTime(Printable):
    FIELDS = ["hours", "minutes", "seconds"]

    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def concatenate(cls, o1: 'RelativeTime', o2: 'RelativeTime') -> 'RelativeTime':
        new = RelativeTime()

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


class Constant(Printable):
    FIELDS = ["name", "alias", "value"]

    def __init__(self, name, alias=None, value=None):
        self.name = name

        if alias is not None:
            self.alias = alias
        else:
            self.alias = []

        self.value = value

    def get_all(self):
        return [self.name, *self.alias]


class Keyword(Constant):
    pass


class MethodEnum:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"<Method: {self.name}>"

    def __repr__(self):
        return f"<Method: {self.name}>"
