import enum
from enum import Enum, auto

class AbsoluteDateTime:
    def __init__(self, year=None, month=None, day=None):
        self.year = year
        self.month = month
        self.day = day

class AbsoluteClockTime:
    def __init__(self, hour=None, minute=None, second=None):
        self.hour = hour
        self.minute = minute
        self.second = second

class RelativeDate:
    def __init__(self, years=None, months=None, weeks=None, days=None):
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

class RelativeTime:
    def __init__(self, hours=None, minutes=None, seconds=None):
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

class Constant:
    def __init__(self, name, alias=None):
        self.name = name

        if alias is not None:
            self.alias = alias
        else:
            self.alias = []

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
