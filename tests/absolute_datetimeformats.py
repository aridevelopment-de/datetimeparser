import datetime

today = datetime.datetime.today()

tests = [
    "2017.08.03 03:04:05",
    "05.05.2017 03:04:10",
    "10.01.2022",
    "2023.01.10",
    "03:02:10",
    "01.01.2023 05:03",
    "07:16",
    "08:20"
]

validation = [
    datetime.datetime(year=2017, month=8, day=3, hour=3, minute=4, second=5),
    datetime.datetime(year=2017, month=5, day=5, hour=3, minute=4, second=10),
    datetime.datetime(year=2022, month=1, day=10),
    datetime.datetime(year=2023, month=1, day=10),
    datetime.datetime(year=today.year, month=today.month, day=today.day, hour=3, minute=2, second=10),
    datetime.datetime(year=2023, month=1, day=1, hour=5, minute=3),
    datetime.datetime(year=today.year, month=today.month, day=today.day, hour=7, minute=16),
    datetime.datetime(year=today.year, month=today.month, day=today.day, hour=8, minute=20)
]