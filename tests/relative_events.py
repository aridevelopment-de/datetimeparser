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
    "eastern 2010"
]

validation = [
    datetime.datetime(today.year, 12, 25),
    datetime.datetime(today.year, 12, 25),
    datetime.datetime(today.year, 12, 31),
    datetime.datetime(2025, 12, 25)
]