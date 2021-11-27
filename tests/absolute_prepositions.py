import datetime

today = datetime.datetime.today()

tests = [
    "second day after christmas",
    "3rd week of august",
    "4. week of august",
    "1st of august",
    "fifth month of 2021",
    "second day after august",
    "3 months before the fifth week of august",
    "10 days and 2 hours after 3 months before christmas 2020",
    "a day and 3 minutes after 4 months before christmas 2021",
    "3 minutes and 4 hours, 2 seconds after new years eve 2000"
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