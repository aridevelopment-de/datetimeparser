import enum
from enum import Enum, auto

class Printable:
    FIELDS = []

    def __str__(self):
        return f'<{str(self.__class__)} {" ".join("{%s=%s}" % (field, getattr(self, field)) for field in self.FIELDS if getattr(self, field) is not None)}>'

    def __repr__(self):
        return f'<{str(self.__class__)} {" ".join("{%s=%s}" % (field, getattr(self, field)) for field in self.FIELDS if getattr(self, field) is not None)}>'

class AbsoluteDateTime(Printable):
    FIELDS = ["year", "month", "day"]

    def __init__(self, year=0, month=0, day=0):
        self.year = year
        self.month = month
        self.day = day

class AbsoluteClockTime(Printable):
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
    def from_keyword(cls, keyword, delta=1):
        if keyword == DatetimeConstants.DAYS:
            return RelativeDate(days=delta)
        elif keyword == DatetimeConstants.WEEKS:
            return RelativeDate(weeks=delta)
        elif keyword == DatetimeConstants.MONTHS:
            return RelativeDate(months=delta)
        elif keyword == DatetimeConstants.YEARS:
            return RelativeDate(years=delta)

class RelativeTime(Printable):
    FIELDS = ["hours", "minutes", "seconds"]

    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def from_keyword(cls, keyword, delta=1):
        if keyword == DatetimeConstants.SECONDS:
            return RelativeTime(seconds=delta)
        elif keyword == DatetimeConstants.MINUTES:
            return RelativeTime(minutes=delta)
        elif keyword == DatetimeConstants.HOURS:
            return RelativeTime(hours=delta)

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

class Constants:
    CHRISTMAS = Constant('christmas', ['next christmas', 'xmas', 'next xmas'])
    SILVESTER = Constant('silvester', ['next silvester', 'new years eve', 'next new years eve'])
    EASTERN = Constant('eastern', ['next eastern', 'easter', 'next easter'])
    NICHOLAS = Constant('nicholas', ['next nicholas', 'nicholas day', 'next nicholas day'])

    ALL = [CHRISTMAS, SILVESTER, EASTERN, NICHOLAS]

class NumberConstants:
    # TODO: Add up to 31?
    ONE = Constant('one', value=1)
    TWO = Constant('two', value=2)
    THREE = Constant('three', value=3)
    FOUR = Constant('four', value=4)
    FIVE = Constant('five', value=5)
    SIX = Constant('six', value=6)
    SEVEN = Constant('seven', value=7)
    EIGHT = Constant('eight', value=8)
    NINE = Constant('nine', value=9)
    TEN = Constant('ten', value=10)

    ALL = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN]

class NumberCountConstants:
    # TODO: Add up to 31?
    FIRST = Constant('first', ['1st', '1.'], value=1)
    SECOND = Constant('second', ['2nd', '2.'], value=2)
    THIRD = Constant('third', ['3rd', '3.'], value=3)
    FOURTH = Constant('fourth', ['4th', '4.'], value=4)
    FIFTH = Constant('fifth', ['5th', '5.'], value=5)
    SIXTH = Constant('sixth', ['6th', '6.'], value=6)
    SEVENTH = Constant('seventh', ['7th', '7.'], value=7)
    EIGHTH = Constant('eighth', ['8th', '8.'], value=8)
    NINTH = Constant('ninth', ['9th', '9.'], value=9)
    TENTH = Constant('tenth', ['10th', '10.'], value=10)

    ALL = [FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVENTH, EIGHTH, NINTH, TENTH]

class DatetimeConstants:
    SECONDS = Keyword('seconds', ['second', 'sec', 'secs'])
    MINUTES = Keyword('minutes', ['minute', 'min', 'mins'])
    HOURS = Keyword('hours', ['hour'])
    DAYS = Keyword('days', ['day'])
    WEEKS = Keyword('weeks', ['week'])
    MONTHS = Keyword('months', ['month'])
    YEARS = Keyword('years', ['year'])

    TIME = [SECONDS, MINUTES, HOURS]
    DATE = [DAYS, WEEKS, MONTHS, YEARS]
    ALL = [SECONDS, MINUTES, HOURS, DAYS, WEEKS, MONTHS, YEARS]

class WeekdayConstants:
    MONDAY = Constant('monday')
    TUESDAY = Constant('tuesday')
    WEDNESDAY = Constant('wednesday')
    THURSDAY = Constant('thursday')
    FRIDAY = Constant('friday')
    SATURDAY = Constant('saturday')
    SUNDAY = Constant('sunday')

    ALL = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]

class MonthConstants:
    JANUARY = Constant('january', ['jan'])
    FEBRUARY = Constant('february', ['feb'])
    MARCH = Constant('march', ['mar'])
    APRIL = Constant('april', ['apr'])
    MAY = Constant('may')
    JUNE = Constant('june', ['jun'])
    JULY = Constant('july', ['jul'])
    AUGUST = Constant('august', ['aug'])
    SEPTEMBER = Constant('september', ['sep'])
    OCTOBER = Constant('october', ['oct'])
    NOVEMBER = Constant('november', ['nov'])
    DECEMBER = Constant('december', ['dec'])

    ALL = [JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER]

class Keywords:
    OF = Keyword('of')
    AFTER = Keyword('after')
    BEFORE = Keyword('before')
    NEXT = Keyword('next')
    IN = Keyword('in')
    FOR = Keyword('for')
