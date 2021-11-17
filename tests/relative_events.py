import datetime

today = datetime.datetime.today()

tests = [
    "next christmas",
    "christmas",
    "new years eve",
    "xmas 2025",
    "next friday",
    "next second",
    "last month",
    "next hour",
    "next year",
    "eastern 2010",
    "halloween 2030",
    "next april fools day",
    "thanksgiving",
    "next st patricks day",
    "valentine day 2010",  # fail
    "summer",
    "winter 2021",
    "next spring",
    "begin of fall 2010",
    "summer end",
    "end of winter",
    "end of the spring",
    "end of autumn 2020",
    "begin of advent of code 2022",
    "end of aoc 2022",
    "end of the year"
]

validation = [
    datetime.datetime(today.year, 12, 25),
    datetime.datetime(today.year, 12, 25),
    datetime.datetime(today.year, 12, 31),
    datetime.datetime(2025, 12, 25)
]