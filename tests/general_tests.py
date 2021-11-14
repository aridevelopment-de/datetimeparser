import datetime

today = datetime.datetime.today()

tests = [
    "next 3 years and 2 months"
]

# TODO
"""
Validation cases are a bit difficult because
 - we can't use timedelta (not every year is 356 days long)
 - creating new datetimes would be a bit hard because when adding 11 seconds to the current time (55 seconds)
   this would result in an Error because the seconds have to be in the range of 0..59 seconds
   
Ideas: build my own wrapper
"""

validation = [

]
