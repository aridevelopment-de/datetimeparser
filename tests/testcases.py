from datetime import datetime
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo


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


class Expected:
    TODAY = datetime.strptime(datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")

    def __new__(
            cls, now: bool = False, delta: relativedelta = None, time_sensitive: bool = False,
            year: int = None, month: int = None, day: int = None, hour: int = 0, minute: int = 0, second: int = 0
    ) -> datetime:
        """
        Base class for creating expected times for testcases.

        If no arguments are given, today's date will be used without hours, minutes and seconds.

        :param now: states, if the base time should be this moment (with seconds)
        :param delta: adds a relativedelta time to the base time
        :param time_sensitive: states if a time is behind the current time, that the next year will be used
        :param year: the base year, Default: this year
        :param month: the base month, Default: this month
        :param day: the base day, Default: this day
        :param hour: the base hour, Default: 0
        :param minute: the base minute, Default: 0
        :param second: the base second, Default: 0
        """
        excepted_time: datetime

        if not now:
            excepted_time = datetime(
                year=year or cls.TODAY.year,
                month=month or cls.TODAY.month,
                day=day or cls.TODAY.day,
                hour=hour,
                minute=minute,
                second=second
            )
        else:
            excepted_time = cls.TODAY

        if delta:
            excepted_time += delta

        if time_sensitive and excepted_time <= cls.TODAY:
            excepted_time += relativedelta(years=1)

        return excepted_time


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


testcases = {
    # Absolute datetime formats
    "absolute_datetime_formats": {
        "2017.08.03 03:04:05": Expected(year=2017, month=8, day=3, hour=3, minute=4, second=5),
        "05.05.2017 03:04:10": Expected(year=2017, month=5, day=5, hour=3, minute=4, second=10),
        "10.01.2022": Expected(year=2022, month=1, day=10),
        "2023.01.10": Expected(year=2023, month=1, day=10),
        "03:02:10": Expected(hour=3, minute=2, second=10),
        "01.01.2023 05:03": Expected(year=2023, month=1, day=1, hour=5, minute=3),
        "07:16": Expected(hour=7, minute=16),
        "08:20": Expected(hour=8, minute=20)
    },
    # Absolute prepositions
    "absolute_prepositions": {
        "second day after christmas": Expected(time_sensitive=True, month=12, day=27),
        "3rd week of august": None,  # Removed, because 3rd week of August is different for each year
        "4. week of august": None,  # Same reasoning as above
        "1st of august": Expected(time_sensitive=True, month=8, day=1),
        "fifth month of 2021": Expected(year=2021, month=5, day=1),
        "three days after the fifth of august 2018": Expected(year=2018, month=8, day=8),
        "second day after august": Expected(time_sensitive=True, month=8, day=3),
        "3 months before the fifth week of august 2020": Expected(year=2020, month=5, day=31),
        "10 days and 2 hours after 3 months before christmas 2020": Expected(year=2020, month=10, day=5, hour=2),
        "a day and 3 minutes after 4 months before christmas 2021": Expected(year=2021, month=8, day=26, minute=3),
        "3 minutes and 4 hours, 2 seconds after new years eve 2000": Expected(year=2000, month=12, day=31, hour=4, minute=3, second=2),
        "2 days after christmas 2023": Expected(year=2023, month=12, day=27),
        # GitHub issue #78
        "quarter past 5pm": Expected(hour=17, minute=15),
        "two quarters past 5h": Expected(hour=5, minute=30),
        "one quarter before 10pm": Expected(hour=21, minute=45),
        "ten quarters after 03:01:10am": Expected(hour=5, minute=31, second=10),
        "hour past christmas": Expected(month=12, day=25, hour=1),
        "30 minutes past easter": None,
        # GitHub issue #158
        "30 hours after 30.03.2020": Expected(year=2020, month=3, day=31, hour=6),
        # GitHub issue #176
        "10 days after pi-day": Expected(time_sensitive=True, month=3, day=14, delta=relativedelta(days=10)),
        "10 days before tau day": Expected(time_sensitive=True, month=6, day=28, delta=relativedelta(days=-10)),
    },
    # Relative Datetimes
    "relative_datetimes": {
        "in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds": Expected(now=True, delta=relativedelta(years=1, months=2,
                                                                                                                weeks=3,
                                                                                                                days=4, hours=5,
                                                                                                                minutes=6,
                                                                                                                seconds=7)),
        "in a year and in 2 months, in 3 seconds and 4 days": Expected(now=True, delta=relativedelta(years=1, months=2, days=4, seconds=3)),
        "for a year": Expected(now=True, delta=relativedelta(years=1)),
        "next 3 years and 2 months": Expected(now=True, delta=relativedelta(years=3, months=2)),
        "in 2d, 500 h 2 seconds and 4 minutes": Expected(now=True, delta=relativedelta(days=2, hours=500, minutes=4, seconds=2)),
        "for 2 days and 1 year": Expected(now=True, delta=relativedelta(years=1, days=2)),
        "1 year 10 seconds": Expected(now=True, delta=relativedelta(years=1, seconds=10)),
        "two years 3 minutes and 1 hour": Expected(now=True, delta=relativedelta(years=2, hours=1, minutes=3)),
        "next 2 years": Expected(now=True, delta=relativedelta(years=2)),
        "last 4 years": Expected(now=True, delta=relativedelta(years=-4)),
        "next three months": Expected(now=True, delta=relativedelta(months=3)),
        "today": Expected(),
        "now": Expected(now=True),
        # GitHub issue #45
        "after lunchtime": None
    },
    # Constants
    "constants": {
        "next christmas": Expected(time_sensitive=True, month=12, day=25),
        "at the next christmas": Expected(time_sensitive=True, month=12, day=25),
        "the next christmas": Expected(time_sensitive=True, month=12, day=25),
        "christmas": Expected(time_sensitive=True, month=12, day=25),
        "new years eve": Expected(time_sensitive=True, month=12, day=31),
        "xmas 2025": Expected(year=2025, month=12, day=25),
        "next friday": None,
        "next second": Expected(now=True, delta=relativedelta(seconds=1)),
        "last month": Expected(now=True, delta=relativedelta(months=-1)),
        "next hour": Expected(now=True, delta=relativedelta(hours=1)),
        "next year": Expected(now=True, delta=relativedelta(years=1)),
        "eastern 2010": Expected(year=2010, month=4, day=4),
        "halloween 2030": Expected(year=2030, month=10, day=31),
        "next april fools day": Expected(time_sensitive=True, month=4, day=1),
        "thanksgiving": Expected(time_sensitive=True, month=11, day=23),
        "next st patricks day": Expected(time_sensitive=True, month=3, day=17),
        "valentine day 2010": Expected(year=2010, month=2, day=14),
        "summer": Expected(time_sensitive=True, month=6, day=1),
        "winter 2021": Expected(year=2021, month=12, day=1),
        "next spring": Expected(time_sensitive=True, month=3, day=1),
        "begin of fall 2010": Expected(year=2010, month=9, day=1),
        "summer end": Expected(time_sensitive=True, month=8, day=31, hour=23, minute=59, second=59),
        f"end of winter {datetime.today().year}": Expected(year=datetime.today().year, month=2, day=28 + is_leap_year(datetime.today().year),
                                                           hour=23, minute=59, second=59),
        "end of the spring": Expected(time_sensitive=True, month=5, day=31, hour=23, minute=59, second=59),
        "end of autumn 2020": Expected(year=2020, month=11, day=30, hour=23, minute=59, second=59),
        "begin of advent of code 2022": Expected(year=2022, month=12, day=1, hour=6),
        "end of aoc 2022": Expected(year=2022, month=12, day=26, hour=6),
        "end of the year": Expected(time_sensitive=True, month=12, day=31, hour=23, minute=59, second=59),
        # GitHub issue #176
        "piday": Expected(time_sensitive=True, month=3, day=14),
        "tauday": Expected(time_sensitive=True, month=6, day=28),
        # GitHub issue #45
        "in the morning": None,
        "in the evening": None,
    },
    # Constant Relative Extensions
    "constants_relative_expressions": {
        "daylight change tomorrow": Expected(hour=6, delta=relativedelta(days=1)),
        "daylight change yesterday": Expected(hour=6, delta=relativedelta(days=-1)),
        "daylight change 01.01.2022": Expected(year=2022, month=1, day=1, hour=6),
        "monday in two weeks": None,
        "tuesday in two years": None,
        "tomorrow 12 o'clock": Expected(hour=12, delta=relativedelta(days=1)),
        "tomorrow at 7pm": Expected(hour=19, delta=relativedelta(days=1)),
        "tomorrow at 17h": Expected(hour=17, delta=relativedelta(days=1)),
        "tomorrow at 17:13": Expected(hour=17, minute=13, delta=relativedelta(days=1)),
        "tomorrow at 17": Expected(hour=17, delta=relativedelta(days=1)),
        "tomorrow afternoon": Expected(hour=15, delta=relativedelta(days=1)),
        "at the next afternoon at tomorrow": Expected(hour=15, delta=relativedelta(days=1)),
        "the day before yesterday": Expected(delta=relativedelta(days=-2)),
        "the day after tomorrow": Expected(delta=relativedelta(days=2)),
        "a day before yesterday": Expected(delta=relativedelta(days=-2)),
        "a day after tomorrow": Expected(delta=relativedelta(days=2)),
        "day before yesterday": Expected(delta=relativedelta(days=-2)),
        "day after tomorrow": Expected(delta=relativedelta(days=2)),
        "two days after tomorrow": Expected(delta=relativedelta(days=3)),
        "two days before yesterday": Expected(delta=relativedelta(days=-3)),
    },
    # Datetime Delta
    "datetime_delta": {
        "at 9pm": Expected(hour=21),
        "at 9:00pm": Expected(hour=21),
        "at 10 in the evening": Expected(hour=22),
        "5 in the morning": Expected(hour=5),
    },
    # Special testcases
    "special": {
        "infinity": ThrowException,
        "inf": ThrowException
    }
}
