# datetimeparser

A datetime parser in Python by Ari24-cb24 and NekoFantic

V 1.0

## Erinnerung für den Parser
- Auf falsche Eingaben überprüfen

## List of events

- ``christmas (next christmas, xmas, next xmas)``: 24.12.YYYY
- ``silvester (next silvester, new years eve, next new years eve)`` 31.12.YYYY
- ``eastern (next eastern, easter, next easter)``: DD.04.YYYY
- ``nicholas (next nicholas, nicholas day, next nicholas day)``: 05.12.YYYY
- ``halloween (next halloween)``: 31.10.YYYY
- ``valentines [valentines/valentine](next valentines, valentines day, next valentines day)``: 14.02.YYYY
- ``april fools day (next april fools day, april fool day, next april fool day)``: 01.04.YYYY
- ``saint patrick's day [saint/st./st][patrick's/patricks](next saint patrick's day)``: 17.03.YYYY
- ``thanksgiving (next thanksgiving)``: 26.11.YYYY
- ``summer begin (summer, next summer, begin of summer, begin of the summer)``
- ``winter begin (winter, next winter, begin of winter, begin of the winter)``
- ``fall begin [fall/autumn](fall, next fall, begin of fall, begin of the fall)``
- ``spring begin (spring, next spring, begin of spring, begin of the spring)``
- ``summer end (end of summer, end of the summer)``
- ``winter end (end of winter, end of the winter)``
- ``fall end [fall/autumn](end of fall, end of the fall)``
- ``spring end (end of spring, end of the spring)``
- ``aoc begin [aoc/advent of code](aoc, next aoc, begin of aoc, begin of the aoc)``
- ``aoc end [aoc/advent of code](end of aoc, end of the aoc)``
- ``end of year (the end of year, the end of the year)``

## Ideen für Datenarchitektur vom Parser zum Evaluator

````python
"""
Absolutes:

[AbsoluteDateTime(year=2020, month=3, day=2)]
[AbsoluteClockTime(hour=3, minute=2, second=1)]
yyyy.mm.dd hh:mm:ss
dd.mm.yyyy hh:mm:ss
hh:mm:ss
dd.mm.yyyy

# Präpositionen: 'Of', 'After', 'Before'
# Rule: first - tenth (nicht weiter gehen)
[RelativeDate(week=3), RelativeTime(), keyword.OF, AbsoluteDateTime(year=2016)]
3rd week of (year) 2016
3rd of august
<1-5>. week of <month>
fifth week of august
1. week of august
1st week of august
2st week of year 2023
1 day after 2025
3 days before august

[RelativeMonth(3), Keyword.BEFORE, RelativeWeek(5), Keyword.OF, AbsoluteMonth.AUGUST]

3 months before the fifth week of august
<monthlyTime> of <constant timespan>
<relativer> after <absoluter>
<relativer> before <absoluter>

[Constant.CHRISTMAS, AbsoluteDateTime(year=2040)]
events (christmas/birth jesus christus, silvester/new years eve, etc)
<event> <specific_time>

# Spezifische Zeit kann noch optional angegeben werden, falls beim Event noch nicht eine solche Zeit definiert wurde
# vor dem Event darf eine Präposition stehen, dann gilt die Kombination aus <Präposition> <Event> als Alias für das Event

[Constant.TOMORROW]
tomorrow


=================================

Relatives:

# Keywords: 'in', 'for', 'last'

[RelativeDate(year=1, month=2, weeks=3, days=4), RelativeTime(hours=5, minutes=6, seconds=7)]
in 1Y 2m 3W 4d 5H 6M 7S
in 1 Year(s) 2 Month(s) 2 Week(s) 4 Day(s) 5 Hour(s) 6 Minute(s) 7 Second(s)
in a year in 2 months in a week in a hour
in 6 min 2 sec
for 1 year
1 year 10 seconds

Preposition: 'next'
[RelativeWeekDay.FRIDAY]
next xyDay
next 3 years
last 3 years


.ban @user next year and 2 months
.ban @user next 1 year
.ban @user next a year

Die Zeitangabe, welche nach der Präposition (in, next) kommt, braucht, wenn die Zeitangabe nur ein einzelnes ist, keine Angabe der Zeit (Siehe Beispiele mit ban)
Für Idioten gesagt: Zeitangabe nach next oder in braucht keine Zahl oder ein `a`

"""
````
