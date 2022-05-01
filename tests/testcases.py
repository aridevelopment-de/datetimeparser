from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytz import timezone


class ThrowException:
    def __str__(self):
        return "ThrowException"

    def __repr__(self):
        return "ThrowException"


class ReturnNone:
    def __str__(self):
        return "ReturnNone"

    def __repr__(self):
        return "ReturnNone"


today = datetime.strptime(datetime.now(tz=timezone("Europe/Berlin")).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

testcases = {
    # Absolute datetime formats
    "absolute_datetime_formats": {
        "2017.08.03 03:04:05": datetime(year=2017, month=8, day=3, hour=3, minute=4, second=5),
        "05.05.2017 03:04:10": datetime(year=2017, month=5, day=5, hour=3, minute=4, second=10),
        "10.01.2022": datetime(year=2022, month=1, day=10),
        "2023.01.10": datetime(year=2023, month=1, day=10),
        "03:02:10": datetime(year=today.year, month=today.month, day=today.day, hour=3, minute=2, second=10),
        "01.01.2023 05:03": datetime(year=2023, month=1, day=1, hour=5, minute=3),
        "07:16": datetime(year=today.year, month=today.month, day=today.day, hour=7, minute=16),
        "08:20": datetime(year=today.year, month=today.month, day=today.day, hour=8, minute=20)
    },
    # Absolute prepositions
    "absolute_prepositions": {
        "second day after christmas": datetime(year=today.year, month=12, day=27),
        "3rd week of august": datetime(year=today.year, month=8, day=22),
        "4. week of august": datetime(year=today.year, month=8, day=29),
        "1st of august": datetime(year=today.year, month=8, day=1),
        "fifth month of 2021": datetime(year=2021, month=5, day=1),
        "three days after the fifth of august 2018": datetime(year=2018, month=8, day=8),
        "second day after august": datetime(year=2022, month=8, day=3),
        "3 months before the fifth week of august 2020": datetime(year=2020, month=5, day=31),
        "10 days and 2 hours after 3 months before christmas 2020": datetime(year=2020, month=10, day=5, hour=2),
        "a day and 3 minutes after 4 months before christmas 2021": datetime(year=2021, month=8, day=26, minute=3),
        "3 minutes and 4 hours, 2 seconds after new years eve 2000": datetime(year=2000, month=12, day=31, hour=4,
                                                                              minute=3, second=2),
        "2 days after christmas 2023": datetime(year=2023, month=12, day=27),
        # GitHub issue #78
        "quarter past 5pm": datetime(today.year, today.month, today.day, 17, 15, 0),
        "two quarters past 5h": datetime(today.year, today.month, today.day, 5, 30, 0),
        "one quarter before 10pm": datetime(today.year, today.month, today.day, 21, 45, 0),
        "ten quarters after 03:01:10am": datetime(today.year, today.month, today.day, 5, 31, 10),
        "hour past christmas": datetime(today.year, 12, 25, 1),
        "30 minutes past easter": None,
        # GitHub issue #158
        "30 hours after 30.03.2020": datetime(year=2020, month=3, day=31, hour=6)
    },
    # Relative Datetimes
    "relative_datetimes": {
        "in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds": today + relativedelta(years=1, months=2,
                                                                                               weeks=3,
                                                                                               days=4, hours=5,
                                                                                               minutes=6,
                                                                                               seconds=7),
        "in a year and in 2 months, in 3 seconds and 4 days": today + relativedelta(years=1, months=2, days=4,
                                                                                    seconds=3),
        "for a year": today + relativedelta(years=1),
        "next 3 years and 2 months": today + relativedelta(years=3, months=2),
        "in 2d, 500 h 2 seconds and 4 minutes": today + relativedelta(days=2, hours=500, minutes=4, seconds=2),
        "for 2 days and 1 year": today + relativedelta(years=1, days=2),
        "1 year 10 seconds": today + relativedelta(years=1, seconds=10),
        "two years 3 minutes and 1 hour": today + relativedelta(years=2, hours=1, minutes=3),
        "next 2 years": today + relativedelta(years=2),
        "last 4 years": today + relativedelta(years=-4),
        "next three months": today + relativedelta(months=3),
        "today": datetime(today.year, today.month, today.day),
        "now": today,
    },
    # Constants
    "constants": {
        "next christmas": datetime(today.year, 12, 25),
        "at the next christmas": datetime(today.year, 12, 25),
        "the next christmas": datetime(today.year, 12, 25),
        "christmas": datetime(today.year, 12, 25),
        "new years eve": datetime(today.year, 12, 31),
        "xmas 2025": datetime(2025, 12, 25),
        "next friday": None,
        "next second": today + relativedelta(seconds=1),
        "last month": today + relativedelta(months=-1),
        "next hour": today + relativedelta(hours=1),
        "next year": today + relativedelta(years=1),
        "eastern 2010": datetime(2010, 4, 4),
        "halloween 2030": datetime(2030, 10, 31),
        "next april fools day": datetime(2023, 4, 1),
        "thanksgiving": datetime(year=today.year, month=11, day=24),
        "next st patricks day": datetime(year=2023, month=3, day=17),
        "valentine day 2010": datetime(2010, 2, 14),
        "summer": datetime(today.year, 6, 1),
        "winter 2021": datetime(2021, 12, 1),
        "next spring": datetime(2023, 3, 1),
        "begin of fall 2010": datetime(2010, 9, 1),
        "summer end": datetime(today.year, 8, 31, 23, 59, 59),
        "end of winter": datetime(2023, 2, 28, 23, 59, 59),
        "end of the spring": datetime(today.year, 5, 31, 23, 59, 59),
        "end of autumn 2020": datetime(2020, 11, 30, 23, 59, 59),
        "begin of advent of code 2022": datetime(2022, 12, 1, 6),
        "end of aoc 2022": datetime(2022, 12, 26, 6),
        "end of the year": datetime(today.year, 12, 31, 23, 59, 59),
    },
    # Constant Relative Extensions
    "constants_relative_expressions": {
        "daylight change tomorrow": datetime(today.year, today.month, today.day, 6) + relativedelta(days=1),
        "daylight change yesterday": datetime(today.year, today.month, today.day, 6) + relativedelta(days=-1),
        "daylight change 01.01.2022": datetime(2022, 1, 1, 6),
        "monday in two weeks": None,
        "tuesday in two years": None,
        "tomorrow 12 o'clock": datetime(today.year, today.month, today.day, 12) + relativedelta(days=1),
        "tomorrow at 7pm": datetime(today.year, today.month, today.day, 19) + relativedelta(days=1),
        "tomorrow at 17h": datetime(today.year, today.month, today.day, 17) + relativedelta(days=1),
        "tomorrow at 17:13": datetime(today.year, today.month, today.day, 17, 13) + relativedelta(days=1),
        "tomorrow at 17": datetime(today.year, today.month, today.day, 17) + relativedelta(days=1),
        "tomorrow afternoon": datetime(today.year, today.month, today.day, 15) + relativedelta(days=1),
        "at the next afternoon at tomorrow": datetime(today.year, today.month, today.day, 15) + relativedelta(days=1),
        "the day before yesterday": datetime(today.year, today.month, today.day) + relativedelta(days=-2),
        "the day after tomorrow": datetime(today.year, today.month, today.day) + relativedelta(days=2),
        "a day before yesterday": datetime(today.year, today.month, today.day) + relativedelta(days=-2),
        "a day after tomorrow": datetime(today.year, today.month, today.day) + relativedelta(days=2),
        "day before yesterday": datetime(today.year, today.month, today.day) + relativedelta(days=-2),
        "day after tomorrow": datetime(today.year, today.month, today.day) + relativedelta(days=2),
        "two days after tomorrow": datetime(today.year, today.month, today.day) + relativedelta(days=3),
        "two days before yesterday": datetime(today.year, today.month, today.day) + relativedelta(days=-3),
    },
    # Datetime Delta
    "datetime_delta": {
        "at 9pm": datetime(today.year, today.month, today.day, 21),
        "at 9:00pm": datetime(today.year, today.month, today.day, 21),
        "at 10 in the evening": datetime(today.year, today.month, today.day, 22),
        "5 in the morning": datetime(today.year, today.month, today.day, 5),
    },
    # Special testcases
    "special": {
        "infinity": ThrowException,
        "inf": ThrowException
    }
}
