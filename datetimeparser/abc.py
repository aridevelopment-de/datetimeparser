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

class RelativeTime:
    def __init__(self, hours=None, minutes=None, seconds=None):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

class RelativeWeekDay:
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

class Constant:
    def __init__(self, name, alias):
        self.name = name
        self.alias = alias

class Constants:
    CHRISTMAS = Constant('christmas', ['next christmas', 'xmas', 'next xmas'])
    SILVESTER = Constant('silvester', ['next silvester', 'new years eve', 'next new years eve'])
    EASTERN = Constant('eastern', ['next eastern', 'easter', 'next easter'])
    NICHOLAS = Constant('nicholas', ['next nicholas', 'nicholas day', 'next nicholas day'])