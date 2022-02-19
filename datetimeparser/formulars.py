from datetime import datetime, timedelta


def eastern_calc(year_time: int) -> datetime:
    a = year_time % 19
    k = year_time // 100
    m = 15 + (3 * k + 3) // 4 - (8 * k + 13) // 25
    d = (19 * a + m) % 30
    s = 2 - (3 * k + 3) // 4
    r = d // 29 + (d // 28 - d // 29) * (a // 11)
    og = 21 + d + r
    sz = 7 - (year_time + year_time // 4 + s) % 7
    oe = 7 - (og - sz) % 7
    os = og + oe

    if os > 32:
        return datetime(year=year_time, month=4, day=(os - 31))
    else:
        return datetime(year=year_time, month=3, day=os)


def thanksgiving_calc(year_time: int) -> datetime:
    year_out = datetime(year=year_time, month=11, day=29)
    date_out = datetime(year=year_time, month=11, day=3)
    return year_out - timedelta(days=(date_out.weekday() + 2))


def days_feb(year_time: int) -> int:
    if int(year_time) % 400 == 0 or int(year_time) % 4 == 0 and not int(year_time) % 100 == 0:
        return 29
    else:
        return 28


def year_start(year_time: int) -> datetime:
    return datetime(year=year_time, month=1, day=1)
