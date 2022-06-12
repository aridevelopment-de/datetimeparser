from datetime import datetime, timedelta
from enum import Enum, auto

from dateutil.relativedelta import relativedelta

from .baseclasses import Constant, MethodEnum
from .formulars import days_feb, eastern_calc, thanksgiving_calc, year_start


class ConstantOption(Enum):
    TIME_VARIABLE = auto()
    DATE_VARIABLE = auto()
    YEAR_VARIABLE = auto()


class Constants:
    CHRISTMAS = Constant('christmas', ['xmas'], options=[ConstantOption.YEAR_VARIABLE],
                         time_value=lambda year_time: datetime(year=year_time, month=12, day=25))
    HOLY_EVE = Constant('holy eve', options=[ConstantOption.YEAR_VARIABLE],
                        time_value=lambda year_time: datetime(year=year_time, month=12, day=24))
    SILVESTER = Constant('silvester', ['new years eve'], options=[ConstantOption.YEAR_VARIABLE],
                         time_value=lambda year_time: datetime(year=year_time, month=12, day=31))
    EASTERN = Constant('eastern', ['easter'], options=[ConstantOption.YEAR_VARIABLE], time_value=eastern_calc)
    NICHOLAS = Constant('nicholas', ['nicholas day'], options=[ConstantOption.YEAR_VARIABLE],
                        time_value=lambda year_time: datetime(year=year_time, month=12, day=6))
    HALLOWEEN = Constant('halloween', options=[ConstantOption.YEAR_VARIABLE],
                         time_value=lambda year_time: datetime(year=year_time, month=10, day=31))
    APRIL_FOOLS_DAY = Constant('april fools day', ['april fool day'], options=[ConstantOption.YEAR_VARIABLE],
                               time_value=lambda year_time: datetime(year=year_time, month=4, day=1))
    THANKSGIVING = Constant('thanksgiving', options=[ConstantOption.YEAR_VARIABLE], time_value=thanksgiving_calc)
    SAINT_PATRICKS_DAY = Constant('saint patrick\'s day',
                                  ['saint patricks day', 'st. patrick\'s day', 'saint pt. day', 'st patrick\'s day', 'st patricks day'],
                                  options=[ConstantOption.YEAR_VARIABLE],
                                  time_value=lambda year_time: datetime(year=year_time, month=3, day=17))
    VALENTINES_DAY = Constant('valentines day', ['valentine', 'valentine day'], options=[ConstantOption.YEAR_VARIABLE],
                              time_value=lambda year_time: datetime(year=year_time, month=2, day=14))
    PI_DAY = Constant("pi day", ["piday", "pi-day"], options=[ConstantOption.YEAR_VARIABLE],
                      time_value=lambda year_time: datetime(year=year_time, month=3, day=14))
    TAU_DAY = Constant("tau day", ["tauday", "tau-day"], options=[ConstantOption.YEAR_VARIABLE],
                       time_value=lambda year_time: datetime(year=year_time, month=6, day=28))

    SUMMER_BEGIN = Constant('summer begin', ['summer', 'begin of summer', 'begin of the summer'], options=[ConstantOption.YEAR_VARIABLE],
                            time_value=lambda year_time: datetime(year=year_time, month=6, day=1))
    WINTER_BEGIN = Constant('winter begin', ['winter', 'begin of winter', 'begin of the winter'], options=[ConstantOption.YEAR_VARIABLE],
                            time_value=lambda year_time: datetime(year=year_time, month=12, day=1))
    SPRING_BEGIN = Constant('spring begin', ['spring', 'begin of spring', 'begin of the spring'], options=[ConstantOption.YEAR_VARIABLE],
                            time_value=lambda year_time: datetime(year=year_time, month=3, day=1))
    FALL_BEGIN = Constant('fall begin',
                          ['fall', 'begin of fall', 'begin of the fall', 'autumn begin', 'autumn', 'begin of autumn',
                           'begin of the autumn'],
                          options=[ConstantOption.YEAR_VARIABLE], time_value=lambda year_time: datetime(year=year_time, month=9, day=1))
    SUMMER_END = Constant('summer end', ['end of summer', 'end of the summer'], options=[ConstantOption.YEAR_VARIABLE],
                          time_value=lambda year_time: datetime(year=year_time, month=8, day=31, hour=23, minute=59, second=59))
    WINTER_END = Constant('winter end', ['end of winter', 'end of the winter'], options=[ConstantOption.YEAR_VARIABLE],
                          time_value=lambda year_time: datetime(year=year_time, month=2, day=days_feb(year_time), hour=23, minute=59,
                                                                second=59))
    SPRING_END = Constant('spring end', ['end of spring', 'end of the spring'], options=[ConstantOption.YEAR_VARIABLE],
                          time_value=lambda year_time: datetime(year=year_time, month=5, day=31, hour=23, minute=59, second=59))
    FALL_END = Constant('fall end', ['end of fall', 'end of the fall', 'autumn end', 'end of autumn', 'end of the autumn'],
                        options=[ConstantOption.YEAR_VARIABLE],
                        time_value=lambda year_time: datetime(year=year_time, month=11, day=30, hour=23, minute=59, second=59))

    MORNING = Constant('morning', ['at morning'],
                       options=[ConstantOption.YEAR_VARIABLE, ConstantOption.DATE_VARIABLE])
    EVENING = Constant('evening', ['at evening'],
                       options=[ConstantOption.YEAR_VARIABLE, ConstantOption.DATE_VARIABLE])
    LUNCHTIME = Constant('lunchtime', ['lunch'], options=[ConstantOption.YEAR_VARIABLE, ConstantOption.DATE_VARIABLE])

    # advent of code always starts at midnight 1st december in SET (5 hours negative UTC offset)
    BEGIN_AOC = Constant('aoc begin',
                         ['aoc', 'begin of aoc', 'begin of the aoc', 'advent of code begin', 'advent of code', 'begin of advent of code',
                          'begin of the advent of code'],
                         options=[ConstantOption.YEAR_VARIABLE],
                         time_value=lambda year_time: datetime(year=year_time, month=12, day=1, hour=0),
                         offset=-5)
    END_AOC = Constant('aoc end',
                       ['end of aoc', 'end of the aoc', 'advent of code end', 'end of advent of code', 'end of the advent of code'],
                       options=[ConstantOption.YEAR_VARIABLE],
                       time_value=lambda year_time: datetime(year=year_time, month=12, day=26, hour=0),
                       offset=-5)

    END_OF_YEAR = Constant('end of year', ['the end of year', 'the end of the year', 'end of the year'],
                           options=[ConstantOption.YEAR_VARIABLE],
                           time_value=lambda year_time: datetime(year=year_time, month=12, day=31, hour=23, minute=59, second=59))
    BEGIN_OF_YEAR = Constant('begin of year', ['the begin of year', 'the begin of the year', 'begin of the year'],
                             options=[ConstantOption.YEAR_VARIABLE], time_value=year_start)

    INFINITY = Constant('infinity', ['inf'], value=None)

    TODAY = Constant('today', options=[ConstantOption.TIME_VARIABLE],
                     time_value=lambda _: datetime(datetime.today().year, datetime.today().month, datetime.today().day))
    TOMORROW = Constant('tomorrow', options=[ConstantOption.TIME_VARIABLE],
                        time_value=lambda _: datetime(datetime.today().year, datetime.today().month, datetime.today().day) + relativedelta(
                            days=1))
    YESTERDAY = Constant('yesterday', options=[ConstantOption.TIME_VARIABLE],
                         time_value=lambda _: datetime(datetime.today().year, datetime.today().month, datetime.today().day) - relativedelta(
                             days=1))
    NOW = Constant('now', ['at the moment', 'current time', 'current time now'], time_value=lambda _: datetime.now())

    ALL = [
        CHRISTMAS, HOLY_EVE, SILVESTER, EASTERN, NICHOLAS, HALLOWEEN, APRIL_FOOLS_DAY, THANKSGIVING, SAINT_PATRICKS_DAY, VALENTINES_DAY,
        PI_DAY, TAU_DAY,
        SUMMER_END, WINTER_END, SPRING_END, FALL_END, SUMMER_BEGIN, WINTER_BEGIN, SPRING_BEGIN, FALL_BEGIN,
        MORNING, EVENING, LUNCHTIME,
        BEGIN_AOC, END_AOC,
        END_OF_YEAR, BEGIN_OF_YEAR,
        INFINITY,
        TODAY, TOMORROW, YESTERDAY, NOW
    ]
    ALL_RELATIVE_CONSTANTS = [TODAY, TOMORROW, YESTERDAY, NOW]


class DatetimeDeltaConstants:
    # time_value is a tuple containing (hours, minutes, seconds)
    MIDNIGHT = Constant('midnight', value=0, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (0, 0, 0))
    NIGHT = Constant('night', value=0, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (21, 0, 0))
    MORNING_NIGHT = Constant('morning night', value=0, options=[ConstantOption.DATE_VARIABLE],
                             time_value=lambda _: (3, 0, 0))
    DAYLIGHT_CHANGE = Constant('daylight change', ['daylight saving', 'daylight saving time'], value=0,
                               options=[ConstantOption.YEAR_VARIABLE, ConstantOption.DATE_VARIABLE],
                               time_value=lambda _: (6, 0, 0))
    SUNRISE = Constant('sunrise', value=0, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (7, 0, 0))
    MORNING = Constant('morning', value=0, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (6, 0, 0))
    BREAKFAST = Constant('breakfast', value=0, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (8, 0, 0))

    MIDDAY = Constant('midday', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (12, 0, 0))
    LUNCH = Constant('lunch', ['lunchtime'], value=12, options=[ConstantOption.DATE_VARIABLE],
                     time_value=lambda _: (12, 0, 0))
    AFTERNOON = Constant('afternoon', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (15, 0, 0))
    EVENING = Constant('evening', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (18, 0, 0))
    DINNER = Constant('dinner', ['dinnertime'], value=12, options=[ConstantOption.DATE_VARIABLE],
                      time_value=lambda _: (19, 0, 0))
    DAWN = Constant('dawn', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (6, 0, 0))
    DUSK = Constant('dusk', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (20, 0, 0))
    SUNSET = Constant('sunset', value=12, options=[ConstantOption.DATE_VARIABLE], time_value=lambda _: (18, 30, 0))

    ALL = [
        MORNING, AFTERNOON, EVENING, NIGHT, MORNING_NIGHT, DAYLIGHT_CHANGE, MIDNIGHT, MIDDAY, DAWN, DUSK,
        SUNRISE, SUNSET, LUNCH, DINNER, BREAKFAST
    ]


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
    TWENTY_ONE = Constant('twenty one', alias=["twentyone", "twenty-one"], value=21)
    TWENTY_TWO = Constant('twenty two', alias=["twentytwo", "twenty-two"], value=22)
    TWENTY_THREE = Constant('twenty three', alias=["twentythree", "twenty-three"], value=23)
    TWENTY_FOUR = Constant('twenty four', alias=["twentyfour", "twenty-four"], value=24)
    TWENTY_FIVE = Constant('twenty five', alias=["twentyfive", "twenty-five"], value=25)
    TWENTY_SIX = Constant('twenty six', alias=["twentysix", "twenty-six"], value=26)
    TWENTY_SEVEN = Constant('twenty seven', alias=["twentyseven", "twenty-seven"], value=27)
    TWENTY_EIGHT = Constant('twenty eight', alias=["twentyeight", "twenty-eight"], value=28)
    TWENTY_NINE = Constant('twenty nine', alias=["twentynine", "twenty-nine"], value=29)
    THIRTY = Constant('thirty', value=30)
    THIRTY_ONE = Constant('thirty one', alias=["thirtyone", "thirty-one"], value=31)

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
    TWENTY_FIRST = Constant('twenty first', alias=['21st', '21.', 'twentyfirst', 'twenty-first'], value=21)
    TWENTY_SECOND = Constant('twenty second', alias=['22nd', '22.', 'twentysecond', 'twenty-second'], value=22)
    TWENTY_THIRD = Constant('twenty third', alias=['23rd', '23.', 'twentythird', 'twenty-third'], value=23)
    TWENTY_FOURTH = Constant('twenty fourth', alias=['24th', '24.', 'twentyfourth', 'twenty-fourth'], value=24)
    TWENTY_FIFTH = Constant('twenty fifth', alias=['25th', '25.', 'twentyfifth', 'twenty-fifth'], value=25)
    TWENTY_SIXTH = Constant('twenty sixth', alias=['26th', '26.', 'twentysixth', 'twenty-sixth'], value=26)
    TWENTY_SEVENTH = Constant('twenty seventh', alias=['27th', '27.', 'twentyseventh', 'twenty-seventh'], value=27)
    TWENTY_EIGHTH = Constant('twenty eighth', alias=['28th', '28.', 'twentyeighth', 'twenty-eighth'], value=28)
    TWENTY_NINTH = Constant('twenty ninth', alias=['29th', '29.', 'twentyninth', 'twenty-ninth'], value=29)
    THIRTIETH = Constant('thirtieth', alias=['30th', '30.'], value=30)
    THIRTY_FIRST = Constant('thirty first', alias=['31st', '31.', 'thirthyfirst', "thirty-first"], value=31)

    # Reversed to avoid conflicts with other constants
    ALL = [FIRST, SECOND, THIRD, FOURTH, FIFTH, SIXTH, SEVENTH, EIGHTH, NINTH, TENTH,
           ELEVENTH, TWELFTH, THIRTEENTH, FOURTEENTH, FIFTEENTH, SIXTEENTH, SEVENTEENTH, EIGHTEENTH, NINETEENTH, TWENTIETH,
           TWENTY_FIRST, TWENTY_SECOND, TWENTY_THIRD, TWENTY_FOURTH, TWENTY_FIFTH, TWENTY_SIXTH, TWENTY_SEVENTH, TWENTY_EIGHTH,
           TWENTY_NINTH,
           THIRTIETH, THIRTY_FIRST][::-1]


class DatetimeConstants:
    SECONDS = Constant('seconds', ['second', 'sec', 'secs'])
    MINUTES = Constant('minutes', ['minute', 'min', 'mins'])
    QUARTERS = Constant('quarters', ['quarter', 'qtr', 'qtrs'])
    HOURS = Constant('hours', ['hour'])
    DAYS = Constant('days', ['day'])
    WEEKS = Constant('weeks', ['week'])
    MONTHS = Constant('months', ['month'])
    YEARS = Constant('years', ['year'])
    OLYMPIADS = Constant('olympiads', ['olympiad'])  # 4 years
    DECADES = Constant('decades', ['decade'])  # 10 years
    CENTURIES = Constant('centuries', ['century'])  # 100 years
    MILLENNIUMS = Constant('millenniums', ['millennium'])  # 1,000 years
    MEGAANNUMS = Constant('megaannuums', ['megaannuum'])  # 1,000,000 years
    GIGAANNUMS = Constant('gigaannuums', ['gigaannuum'])  # 1,000,000,000 years

    TIME = [SECONDS, MINUTES, QUARTERS, HOURS]
    DATE = [DAYS, WEEKS, MONTHS, YEARS, DECADES, CENTURIES, MILLENNIUMS, MEGAANNUMS, GIGAANNUMS]
    ALL = [*DATE, *TIME]

    @classmethod
    def convert_from_mini_date(cls, md):
        if md.lower() == "s":
            return cls.SECONDS
        elif md.lower() == "m":
            return cls.MINUTES
        elif md.lower() == "h":
            return cls.HOURS
        elif md.lower() == "w":
            return cls.WEEKS
        elif md.lower() == "d":
            return cls.DAYS
        elif md.lower() == "y":
            return cls.YEARS


class WeekdayConstants:
    MONDAY = Constant('monday', time_value=lambda date: f"{date + timedelta((0 - date.weekday()) % 7)}")
    TUESDAY = Constant('tuesday', time_value=lambda date: f"{date + timedelta((1 - date.weekday()) % 7)}")
    WEDNESDAY = Constant('wednesday', time_value=lambda date: f"{date + timedelta((2 - date.weekday()) % 7)}")
    THURSDAY = Constant('thursday', time_value=lambda date: f"{date + timedelta((3 - date.weekday()) % 7)}")
    FRIDAY = Constant('friday', time_value=lambda date: f"{date + timedelta((4 - date.weekday()) % 7)}")
    SATURDAY = Constant('saturday', time_value=lambda date: f"{date + timedelta((5 - date.weekday()) % 7)}")
    SUNDAY = Constant('sunday', time_value=lambda date: f"{date + timedelta((6 - date.weekday()) % 7)}")

    ALL = [MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY]


class MonthConstants:
    JANUARY = Constant('january', ['jan'], time_value=lambda year_time: datetime(year=year_time, month=1, day=1))
    FEBRUARY = Constant('february', ['feb'], time_value=lambda year_time: datetime(year=year_time, month=2, day=1))
    MARCH = Constant('march', ['mar'], time_value=lambda year_time: datetime(year=year_time, month=3, day=1))
    APRIL = Constant('april', ['apr'], time_value=lambda year_time: datetime(year=year_time, month=4, day=1))
    MAY = Constant('may', time_value=lambda year_time: datetime(year=year_time, month=5, day=1))
    JUNE = Constant('june', ['jun'], time_value=lambda year_time: datetime(year=year_time, month=6, day=1))
    JULY = Constant('july', ['jul'], time_value=lambda year_time: datetime(year=year_time, month=7, day=1))
    AUGUST = Constant('august', ['aug'], time_value=lambda year_time: datetime(year=year_time, month=8, day=1))
    SEPTEMBER = Constant('september', ['sep'], time_value=lambda year_time: datetime(year=year_time, month=9, day=1))
    OCTOBER = Constant('october', ['oct'], time_value=lambda year_time: datetime(year=year_time, month=10, day=1))
    NOVEMBER = Constant('november', ['nov'], time_value=lambda year_time: datetime(year=year_time, month=11, day=1))
    DECEMBER = Constant('december', ['dec'], time_value=lambda year_time: datetime(year=year_time, month=12, day=1))

    ALL = [JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER]


class Keywords:
    OF = Constant('of')
    AFTER = Constant('after')
    BEFORE = Constant('before')
    NEXT = Constant('next')
    IN = Constant('in')
    FOR = Constant('for')
    PAST = Constant('past')

    ALL = [OF, AFTER, BEFORE, NEXT, IN, FOR, PAST]


class Method:
    ABSOLUTE_PREPOSITIONS = MethodEnum('absolute_prepositions')
    ABSOLUTE_DATE_FORMATS = MethodEnum('absolute_date_formats')
    CONSTANTS = MethodEnum('constants')
    CONSTANTS_RELATIVE_EXTENSIONS = MethodEnum('constants_relative_extensions')
    DATETIME_DELTA_CONSTANTS = MethodEnum('datetime_delta_constants')
    RELATIVE_DATETIMES = MethodEnum('relative_datetimes')
