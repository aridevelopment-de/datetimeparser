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
    def join(cls, o1, o2):
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
    def join(cls, o1, o2):
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
    HALLOWEEN = Constant('halloween', ['next halloween'])
    APRIL_FOOLS_DAY = Constant('april fools day', ['next april fools day', 'april fool day', 'next april fool day'])
    THANKSGIVING = Constant('thanksgiving', ['next thanksgiving'])
    SAINT_PATRICKS_DAY = Constant('saint patrick\'s day', ['next saint patrick\'s day', 'saint patricks day',
                                                           'next saint patricks day', 'st. patrick\'s day',
                                                           'next st. patrick\'s day', 'saint st. day',
                                                           'next st. patricks day', 'st patrick\'s day',
                                                           'next st patrick\'s day', 'st patricks day',
                                                           'next st patricks day'])
    VALENTINES_DAY = Constant('valentines day', ['next valentines day', 'valentine', 'next valentine', 'valentine day', 'next valentine day'])

    SUMMER_BEGIN = Constant('summer begin', ['summer', 'next summer', 'begin of summer', 'begin of the summer'])
    WINTER_BEGIN = Constant('winter begin', ['winter', 'next winter', 'begin of winter', 'begin of the winter', 'winter is coming'])
    SPRING_BEGIN = Constant('spring begin', ['spring', 'next spring', 'begin of spring', 'begin of the spring'])
    FALL_BEGIN = Constant('fall begin', ['fall', 'begin of fall', 'begin of the fall', 'autumn begin', 'autumn',
                                         'begin of autumn', 'begin of the autumn'])
    SUMMER_END = Constant('summer end', ['end of summer', 'end of the summer'])
    WINTER_END = Constant('winter end', ['end of winter', 'end of the winter'])
    SPRING_END = Constant('spring end', ['end of spring', 'end of the spring'])
    FALL_END = Constant('fall end', ['end of fall', 'end of the fall', 'autumn end', 'end of autumn', 'end of the autumn'])

    BEGIN_AOC = Constant('aoc begin', ['aoc', 'next aoc', 'begin of aoc', 'begin of the aoc', 'advent of code begin',
                                       'advent of code', 'next advent of code', 'begin of advent of code',
                                       'begin of the advent of code'])
    END_AOC = Constant('aoc end', ['end of aoc', 'end of the aoc', 'advent of code end', 'end of advent of code',
                                   'end of the advent of code'])

    END_OF_YEAR = Constant('end of year', ['the end of year', 'the end of the year', 'end of the year'])

    INFINITY = Constant('infinity', ['inf', 'NekoFanatic'])

    ALL = [CHRISTMAS, SILVESTER, EASTERN, NICHOLAS, HALLOWEEN, APRIL_FOOLS_DAY, THANKSGIVING, SAINT_PATRICKS_DAY, VALENTINES_DAY,
           SUMMER_END, WINTER_END, SPRING_END, FALL_END, SUMMER_BEGIN, WINTER_BEGIN, SPRING_BEGIN, FALL_BEGIN,
           BEGIN_AOC, END_AOC,
           END_OF_YEAR,
           INFINITY]

class NumberConstants:
    # Presented to you by github copilot
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
    ELEVEN = Constant('eleven', value=11)
    TWELVE = Constant('twelve', value=12)
    THIRTEEN = Constant('thirteen', value=13)
    FOURTEEN = Constant('fourteen', value=14)
    FIFTEEN = Constant('fifteen', value=15)
    SIXTEEN = Constant('sixteen', value=16)
    SEVENTEEN = Constant('seventeen', value=17)
    EIGHTEEN = Constant('eighteen', value=18)
    NINETEEN = Constant('nineteen', value=19)
    TWENTY = Constant('twenty', value=20)
    TWENTY_ONE = Constant('twenty one', alias=["twentyone"], value=21)
    TWENTY_TWO = Constant('twenty two', alias=["twentytwo"], value=22)
    TWENTY_THREE = Constant('twenty three', alias=["twentythree"], value=23)
    TWENTY_FOUR = Constant('twenty four', alias=["twentyfour"], value=24)
    TWENTY_FIVE = Constant('twenty five', alias=["twentyfive"], value=25)
    TWENTY_SIX = Constant('twenty six', alias=["twentysix"], value=26)
    TWENTY_SEVEN = Constant('twenty seven', alias=["twentyseven"], value=27)
    TWENTY_EIGHT = Constant('twenty eight', alias=["twentyeight"], value=28)
    TWENTY_NINE = Constant('twenty nine', alias=["twentynine"], value=29)
    THIRTY = Constant('thirty', value=30)
    THIRTY_ONE = Constant('thirty one', alias=["thirtyone"], value=31)

    # Reversed to avoid conflicts with other constants (one is included in twenty one)
    ALL = [ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN,
           ELEVEN, TWELVE, THIRTEEN, FOURTEEN, FIFTEEN, SIXTEEN, SEVENTEEN, EIGHTEEN, NINETEEN, TWENTY,
           TWENTY_ONE, TWENTY_TWO, TWENTY_THREE, TWENTY_FOUR, TWENTY_FIVE, TWENTY_SIX, TWENTY_SEVEN, TWENTY_EIGHT, TWENTY_NINE,
           THIRTY, THIRTY_ONE][::-1]

class NumberCountConstants:
    # Presented to you by github copilot
    FIRST = Constant('first', alias=['1st', '1.'], value=1)
    SECOND = Constant('second', alias=['2nd', '2.'], value=2)
    THIRD = Constant('third', alias=['3rd', '3.'], value=3)
    FOURTH = Constant('fourth', alias=['4th', '4.'], value=4)
    FIFTH = Constant('fifth', alias=['5th', '5.'], value=5)
    SIXTH = Constant('sixth', alias=['6th', '6.'], value=6)
    SEVENTH = Constant('seventh', alias=['7th', '7.'], value=7)
    EIGHTH = Constant('eighth', alias=['8th', '8.'], value=8)
    NINTH = Constant('ninth', alias=['9th', '9.'], value=9)
    TENTH = Constant('tenth', alias=['10th', '10.'], value=10)
    ELEVENTH = Constant('eleventh', alias=['11th', '11.'], value=11)
    TWELFTH = Constant('twelfth', alias=['12th', '12.'], value=12)
    THIRTEENTH = Constant('thirteenth', alias=['13th', '13.'], value=13)
    FOURTEENTH = Constant('fourteenth', alias=['14th', '14.'], value=14)
    FIFTEENTH = Constant('fifteenth', alias=['15th', '15.'], value=15)
    SIXTEENTH = Constant('sixteenth', alias=['16th', '16.'], value=16)
    SEVENTEENTH = Constant('seventeenth', alias=['17th', '17.'], value=17)
    EIGHTEENTH = Constant('eighteenth', alias=['18th', '18.'], value=18)
    NINETEENTH = Constant('nineteenth', alias=['19th', '19.'], value=19)
    TWENTIETH = Constant('twentieth', alias=['20th', '20.'], value=20)
    TWENTY_FIRST = Constant('twenty first', alias=['21st', '21.', 'twentyfirst'], value=21)
    TWENTY_SECOND = Constant('twenty second', alias=['22nd', '22.', 'twentysecond'], value=22)
    TWENTY_THIRD = Constant('twenty third', alias=['23rd', '23.', 'twentythird'], value=23)
    TWENTY_FOURTH = Constant('twenty fourth', alias=['24th', '24.', 'twentyfourth'], value=24)
    TWENTY_FIFTH = Constant('twenty fifth', alias=['25th', '25.', 'twentyfifth'], value=25)
    TWENTY_SIXTH = Constant('twenty sixth', alias=['26th', '26.', 'twentysixth'], value=26)
    TWENTY_SEVENTH = Constant('twenty seventh', alias=['27th', '27.', 'twentyseventh'], value=27)
    TWENTY_EIGHTH = Constant('twenty eighth', alias=['28th', '28.', 'twentyeighth'], value=28)
    TWENTY_NINTH = Constant('twenty ninth', alias=['29th', '29.', 'twentyninth'], value=29)
    THIRTIETH = Constant('thirtieth', alias=['30th', '30.'], value=30)
    THIRTY_FIRST = Constant('thirty first', alias=['31st', '31.', 'thirthyfirst'], value=31)

    # Reversed to avoid conflicts with other constants
    ALL = [FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVENTH, EIGHTH, NINTH, TENTH,
           ELEVENTH, TWELFTH, THIRTEENTH, FOURTEENTH, FIFTEENTH, SIXTEENTH, SEVENTEENTH, EIGHTEENTH, NINETEENTH, TWENTIETH,
           TWENTY_FIRST, TWENTY_SECOND, TWENTY_THIRD, TWENTY_FOURTH, TWENTY_FIFTH, TWENTY_SIXTH, TWENTY_SEVENTH, TWENTY_EIGHTH, TWENTY_NINTH,
           THIRTIETH, THIRTY_FIRST][::-1]

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

    @classmethod
    def convert_from_mini_date(cls, md):
        if md.lower() == "s":
            return cls.SECONDS
        elif md == "M":
            return cls.MINUTES
        elif md.lower() == "h":
            return cls.HOURS
        elif md.lower() == "w":
            return cls.WEEKS
        elif md == "d":
            return cls.DAYS
        elif md == "m":
            return cls.MONTHS
        elif md.lower() == "y":
            return cls.YEARS

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

class MethodEnum:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"<Method: {self.name}>"

    def __repr__(self):
        return f"<Method: {self.name}>"

class Method:
    ABSOLUTE_PREPOSITIONS = MethodEnum('absolute_prepositions')
    ABSOLUTE_DATE_FORMATS = MethodEnum('absolute_date_formats')
    CONSTANTS = MethodEnum('constants')
    RELATIVE_DATETIMES = MethodEnum('relative_datetimes')
