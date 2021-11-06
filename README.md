# datetimeparser

A datetime parser in Python by Ari24-cb24 and NekoFantic

V 1.0

## Liste an Events

- ``christmas``
````markdown
+ Year configurable

When: 24.12.YYYY

Alias:
- next christmas
- xmas
- next xmas
````

- ``silvester``
````markdown
+ Year configurable

When: 31.12.YYYY

Alias:
- next silvester
- new years eve
- next new years eve
````

- ``eastern``
````markdown
+ Year configurable

When: <NonFixedDay>.04.YYYY

Alias:
- easter
- next eastern
- next easter
````

- nicholas
````markdown
+ Year configurable

When: 05.12.YYYY

Alias:
- next nicholas
- nicholas day
- next nicholas day
`````

## Ideen für Datenarchitektur vom Parser zum Evaluator

````python
"""
Absolutes:

[AbsoluteDateTime(year=1, month=1, day=1), AbsoluteClockTime(hour=1, minute=1, second=1)]

yyyy.mm.dd hh:mm:ss
dd.mm.yyyy hh:mm:ss
hh:mm:ss
dd.mm.yyyy

# Präpositionen: 'Of', 'After', 'Before'
[AbsoluteWeek(3), keyword.OF, AbsoluteYear(2016)]
3rd of august
<1-5>. week of <month>
fifth week of august
1. week of august
1st week of august
2st week of year 2023
1 day after 2025
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

# Keywords: 'next', 'in', 'for'

[RelativeDate(year=1, month=2, weeks=3, days=4), RelativeTime(hours=5, minutes=6, seconds=7)]
in 1Y 2m 3W 4d 5H 6M 7S
in 1 Year(s) 2 Month(s) 2 Week(s) 4 Day(s) 5 Hour(s) 6 Minute(s) 7 Second(s)
in a year in 2 months in a week in a hour
in 6 min 2 sec

[RelativeWeekDay.FRIDAY]
next xyDay

.ban @user next year and 2 months
.ban @user next 1 year
.ban @user next a year

Die Zeitangabe, welche nach der Präposition (in, next) kommt, braucht, wenn die Zeitangabe nur ein einzelnes ist, keine Angabe der Zeit (Siehe Beispiele mit ban)
Für Idioten gesagt: Zeitangabe nach next oder in braucht keine Zahl oder ein `a`

"""
````