import datetime

today = datetime.datetime.today()

tests = [
    "second day after christmas",
    "3rd week of august",
    "4. week of august",
    "1st of august",
    "fifth month of 2021",
    "second day after august",
    "3 months before the fifth week of august"
]

validation = [
    datetime.datetime(year=today.year, month=12, day=25),
    datetime.datetime(year=today.year, month=8, day=21),
    datetime.datetime(year=today.year, month=8, day=28),
    datetime.datetime(year=today.year, month=8, day=1),
    datetime.datetime(year=2021, month=5, day=1),
    datetime.datetime(year=today.year, month=8, day=2),
    datetime.datetime(year=today.year, month=5, day=21)
]