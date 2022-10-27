from datetime import datetime, timedelta
import math


def day_of_year(dt: datetime) -> int:
    n1 = math.floor(275 * dt.month / 9)
    n2 = math.floor((dt.month + 9) / 12)
    n3 = (1 + math.floor((dt.year - 4 * math.floor(dt.year / 4) + 2) / 3))

    return n1 - (n2 * n3) + dt.day - 30


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


def calc_sun_time(dt: datetime, timezone: tuple[float, float, float], sunrise: bool = True) -> datetime:
    """
    Calculates the time for sunrise and sunset based on coordinates and a date
    :param dt: The date for calculating the sunset
    :param timezone: A tuple with longitude and latitude and timezone offset
    :param sunrise: If True the sunrise will be calculated if False the sunset
    :returns: The time for the sunrise/sunset
    """

    to_rad: float = math.pi / 180
    day: int = day_of_year(dt)
    longitude_to_hour = timezone[0] / 15
    b = timezone[1] * to_rad
    h = -50 * to_rad / 60

    time_equation = -0.171 * math.sin(0.0337 * day + 0.465) - 0.1299 * math.sin(0.01787 * day - 0.168)
    declination = 0.4095 * math.sin(0.016906 * (day - 80.086))

    time_difference = 12 * math.acos((math.sin(h) - math.sin(b) * math. sin(declination)) / (math.cos(b) * math.cos(declination))) / math.pi

    if sunrise:  # woz -> True time at location
        woz = 12 - time_difference
    else:
        woz = 12 + time_difference

    time: float = (woz - time_equation) - longitude_to_hour + timezone[2]

    hour: int = int(time)
    minutes_left: float = time - int(time)
    minutes_with_seconds = minutes_left * 60
    minute: int = int(minutes_with_seconds)
    second: int = int((minutes_with_seconds - minute) * 60)

    out: datetime = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour, minute=minute, second=second)

    return out

