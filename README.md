# datetimeparser

A datetime parser in Python by Ari24-cb24 and NekoFantic

V 1.0


### Ideas fürs Konstrukt

````python
"""
Absolutes:

yyyy.mm.dd hh:mm:ss
dd.mm.yyyy hh:mm:ss
hh:mm:ss
dd.mm.yyyy

3rd of august
<1-5> week of <month>
fifth week of august
1. week of august
1st week of august

events (christmas, silvester, etc)

(<relativer> after <absoluter>)
(<relativer> before <absoluter>)

# vor dem Event darf eine Präposition stehen, dann gilt die Kombination aus <Präposition> <Event> als Alias für das Event

tomorrow


=================================

Relatives:

# 2 keywords
# in
# next


in 1Y 2M 3W 4d 5h 6m 7s
in 1 Year(s) 2 Month(s) 2 Week(s) 4 Day(s) 5 Hour(s) 6 Minute(s) 7 Second(s)
in a year in 2 months in a week in a hour
in 6 min 2 sec
next xyDay

.ban @user next year and 2 months
.ban @user next 1 year
.ban @user next a year

Die Zeitangabe, welche nach der Präposition (in, next) kommt, braucht, wenn die Zeitangabe nur ein einzelnes ist, keine Angabe der Zeit (Siehe Beispiele mit ban)
Für Idioten gesagt: Zeitangabe nach next oder in braucht keine Zahl oder ein `a`

"""
````

### Ideen für Datenarchitektur vom Parser zum Evaluator

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

[Constant.CHRISTMAS]

events (christmas, silvester, etc)
# vor dem Event darf eine Präposition stehen, dann gilt die Kombination aus <Präposition> <Event> als Alias für das Event

[Constant.TOMORROW]
tomorrow


=================================

Relatives:

# Keywords: 'next', 'in', 'for'

[RelativeDate(year=1, month=2, weeks=3, days=4), RelativeTime(hours=5, minutes=6, seconds=7)]
in 1Y 2M 3W 4d 5h 6m 7s
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