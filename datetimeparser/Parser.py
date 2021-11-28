import datetime

from .baseclasses import *


class Parser:
    DATETIME_FORMATS = [
        "%Y.%m.%d %H:%M:%S",
        "%d.%m.%Y %H:%M:%S",
        "%Y.%m.%d",
        "%d.%m.%Y",
        "%H:%M:%S",
        "%H:%M",
        "%Y.%m.d %H:%M",
        "%d.%m.%Y %H:%M"
    ]

    CLOCKTIME_FORMATS = [
        "%H:%M:%S",
        "%H:%M"
    ]

    ABSOLUTE_PREPOSITION_TOKENS = [
        Keywords.OF,
        Keywords.AFTER,
        Keywords.BEFORE
    ]

    def __init__(self, string):
        self.string = string

    def parse_absolute_date_formats(self):
        for format_ in self.DATETIME_FORMATS:
            try:
                time = datetime.datetime.strptime(self.string, format_)
                timings = []

                if format_ not in self.CLOCKTIME_FORMATS:
                    timings.append(AbsoluteDateTime(year=time.year, month=time.month, day=time.day))

                timings.append(AbsoluteClockTime(hour=time.hour, minute=time.minute, second=time.second))

                return Method.ABSOLUTE_DATE_FORMATS, timings
            except ValueError:
                continue

        return None

    def __get_absolute_preposition_parts(self, string):
        if not any(kw in string for pr in self.ABSOLUTE_PREPOSITION_TOKENS for kw in pr.get_all()):
            return None

        word = None
        char_count = 0

        for word in string.split():
            char_count += len(word) + 1

            if word.lower() in [kw for pr in self.ABSOLUTE_PREPOSITION_TOKENS for kw in pr.get_all()]:
                break

        relative = string[:char_count - len(word) - 2]
        absolute = string[char_count:]

        if self.__get_absolute_preposition_parts(absolute) is not None:
            absolute = self.__get_absolute_preposition_parts(absolute)

        return {'type': 'relative', 'data': relative}, {'type': 'keyword', 'data': word}, {'type': 'absolute', 'data': absolute}

    def __parse_relative_statement(self, string):
        """
        :param string:
        :return:
        """

        parts = string.split()
        data = []

        """
        kinda the same as parse_relative_datetimes

        a day and 3 minutes after 4 months before christmas 2021
        10 days and 2 hours after xmas
        the 5th day after next christmas

        we'll parse here:

        3 seconds, 2 minutes and 4 hours
        a day and 3 minutes
        10 days and 2 hours
        the 5th day
        the fifth day
        3rd week
        4. week
        """

        for part in parts:
            part = part.strip()

            if part.endswith(","):
                part = part[:-1]

            if part.lower() in ("and", ",", "the"):
                continue

            if part.lower() == "a":
                data.append(1)
                continue

            if part.isnumeric():
                data.append(int(part))
                continue

            found_one = False

            # 1st, 1., first
            for kw in NumberCountConstants.ALL:
                for alias in kw.get_all():
                    if alias == part.lower():
                        data.append(kw.value)
                        found_one = True
                        break
                else:
                    continue

                break

            if found_one:
                continue

            # one, two, three
            for kw in NumberConstants.ALL:
                for alias in kw.get_all():
                    if alias == part.lower():
                        data.append(kw.value)
                        found_one = True
                        break
                else:
                    continue

                break

            if found_one:
                continue

            # date and time
            for kw in DatetimeConstants.ALL:
                for alias in kw.get_all():
                    if alias == part.lower():
                        data.append(kw)
                        break
                else:
                    continue

                break

        return data

    def __parse_absolute_keyword(self, string):
        string = string.lower()

        for pr in self.ABSOLUTE_PREPOSITION_TOKENS:
            for kw in pr.get_all():
                if string == kw:
                    return pr

        raise ValueError('no preposition given')

    def __parse_absolute_statement(self, data):
        if isinstance(data, str):
            """
            Constants
            Years
            Months
            Weekdays
            Constants <year>
            """

            data = data.lower()
            keywords = [*Constants.ALL, *MonthConstants.ALL]

            for keyword in keywords:
                if data in [kw for kw in keyword.get_all()]:
                    return (keyword,)
                else:
                    for kw in keyword.get_all():
                        d = data.split()

                        if d[-1].isnumeric() and " ".join(d[:-1]).lower() == kw:
                            year = int(d[-1])

                            if 1970 < year < 9999:
                                return keyword, AbsoluteDateTime(year=year)
                    else:
                        if data.isnumeric():
                            data = int(data)

                            if 1970 <= data <= 9999:
                                return (AbsoluteDateTime(year=data),)
        else:
            return self.__convert_absolute_preposition_tokens(data)

        return data

    def __convert_absolute_preposition_tokens(self, data):
        new_data = []

        for i, part in enumerate(data):
            if part['type'] == 'relative':
                relative_data = []

                for d in self.__parse_relative_statement(part['data']):
                    relative_data.append(d)

                next_preposition = [*filter(lambda e: e['type'] == 'keyword', data[i:])][0]['data']
                relative_data = self.__convert_absolute_prepositions_better_relative(relative_data, next_preposition)

                for d in relative_data:
                    new_data.append(d)
            elif part['type'] == 'keyword':
                new_data.append(self.__parse_absolute_keyword(part['data']))
            elif part['type'] == 'absolute':
                for d in self.__parse_absolute_statement(part['data']):
                    new_data.append(d)

        return new_data

    @staticmethod
    def __convert_absolute_prepositions_better_relative(tokens, preposition):
        # We currently support every preposition ('after', 'before', 'in')
        if len(tokens) == 1 or len(tokens) % 2 != 0:
            return tokens

        new_tokens = []

        for i in range(0, len(tokens), 2):
            value, unit = tokens[i], tokens[i + 1]

            if isinstance(value, int) and unit in DatetimeConstants.ALL:
                value *= -1 if preposition == 'before' else 1

                if unit in DatetimeConstants.DATE:
                    data = RelativeDate.from_keyword(unit, value)
                elif unit in DatetimeConstants.TIME:
                    data = RelativeTime.from_keyword(unit, value)
                else:
                    raise RuntimeError("Unknown unit:", unit)

                if i == 0:
                    new_tokens.append(data)
                else:
                    if type(new_tokens[-1]) is type(data):
                        token_before = new_tokens.pop()
                        new_obj = token_before.join(token_before, data)
                        new_tokens.append(new_obj)
                    else:
                        new_tokens.append(data)

        return new_tokens

    def parse_absolute_prepositions(self):
        splitted = self.__get_absolute_preposition_parts(self.string)

        if splitted is None:
            return None

        tokens = self.__convert_absolute_preposition_tokens(splitted)

        return Method.ABSOLUTE_PREPOSITIONS, tokens

    def parse_constants(self):
        # It's important that WeekdayConstant goes before DatetimeConstants because `friday` contains the word `day`
        keywords = [*Constants.ALL, *MonthConstants.ALL, *WeekdayConstants.ALL, *DatetimeConstants.ALL]

        for keyword in keywords:
            if self.string.lower() in [kw for kw in keyword.get_all()]:
                # Check if the string is already a constant
                return Method.CONSTANTS, [keyword]
            else:
                for kw in keyword.get_all():
                    if kw in self.string.lower():
                        # Otherwise check for prepositions
                        """
                        It can be only one of the following:
                        last <word>
                        next <word>
                        <word> 2020
                        """
                        data = self.string.split()

                        if data[0].strip().lower() in ('last', 'next') and " ".join(data[1:]).lower() == kw:
                            # preposition
                            # next [friday]
                            """
                            **Don't do next 3 days in here**
                            The above is parsed in relative_datetimes
                            so there is no need to parse it here
                            """

                            preposition = data[0].strip()
                            weekday = keyword

                            number = 0
                            if preposition == "next":
                                number = 1
                            elif preposition == "last":
                                number = -1

                            if weekday in DatetimeConstants.ALL:
                                if weekday in DatetimeConstants.TIME:
                                    return Method.CONSTANTS, [RelativeTime.from_keyword(weekday, delta=number)]
                                elif weekday in DatetimeConstants.DATE:
                                    return Method.CONSTANTS, [RelativeDate.from_keyword(weekday, delta=number)]
                            elif weekday in WeekdayConstants.ALL:
                                return Method.CONSTANTS, [weekday]
                            else:
                                return None

                        elif data[-1].isnumeric() and " ".join(data[:-1]).lower() == kw:
                            # currently only year
                            # xmas 2025

                            year = int(data[-1])

                            if 1970 <= year <= 9999:
                                return Method.CONSTANTS, [keyword, AbsoluteDateTime(year=year)]

    @staticmethod
    def parse_relative_datetimes(data):
        PREPOSITIONS = ["in", "for", "next", "last"]

        preposition = ""

        for preposition in PREPOSITIONS:
            # Even if it doesn't start with a preposition, we still need to check if it's a relative datetime
            if data.startswith(preposition):
                data = data[len(preposition):]
                break
        else:
            preposition = ""

        """
        idea:
        1 Year and 2 months, 3d 5 minutes

        split by space
        ['1', 'Year', 'and', '2', 'months,', '3d', '5', 'minutes']

        go through every element
        if there's a comma at the end of the string:
            cut it away

        if the string is equal to "and":
            continue

        if its numeric [or 'a']:
            append to new list

        if its a written number:
            append value to new list

        if its a valid keyword (year, month, days, minutes, ...):
            append the Keyword to the new list

        if the characters up until the last character (30d -> 30) are numeric and the last character is a valid keyword:
            append the number to new list
            append the keyword to the new list
        """

        data = data.strip().split()
        new_data = []

        for part in data:
            not_possible = True
            part = part.strip()

            # We Skip these 3 "prepositions"
            if part.lower() in ["and", "in", "for", ","]:
                continue

            elif part.lower() == "a":
                new_data.append(1 if preposition != "last" else -1)
                not_possible = False

            elif part.endswith(","):
                part = part[:-1]

            if len(part) == 1:
                keyword = DatetimeConstants.convert_from_mini_date(part)

                if keyword is not None:
                    if not new_data:
                        # If there is no number before the keyword, we need to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)
                    elif not isinstance(new_data[-1], int):
                        # If the element before the keyword is not a number we have to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)

                    new_data.append(keyword)
                    not_possible = False

            if part.isnumeric():
                new_data.append(int(part) if preposition != "last" else -int(part))
                not_possible = False

            for kw in NumberConstants.ALL:
                if part.lower() in kw.get_all():
                    new_data.append(kw.value)
                    not_possible = False
                    break

            for keyword in DatetimeConstants.ALL:
                # Seconds, minutes, ...
                if part.lower() in keyword.get_all():
                    if not new_data:
                        # If there is no number before the keyword, we need to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)
                    elif not isinstance(new_data[-1], int):
                        # If the element before the keyword is not a number we have to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)

                    new_data.append(keyword)
                    not_possible = False
                    break
            else:
                if part[:-1].isnumeric():
                    # 1S, 2Y, 3D, ...
                    number = int(part[:-1]) if preposition != "last" else -int(part[:-1])
                    keyword = part[-1]

                    keyword = DatetimeConstants.convert_from_mini_date(keyword)

                    if keyword is not None:
                        new_data.append(number)
                        new_data.append(keyword)

                        not_possible = False

            if not_possible:
                return None

        date = RelativeDate()
        time = RelativeTime()

        if len(new_data) % 2 != 0:
            return None

        while new_data:
            number = new_data.pop(0)
            type_ = new_data.pop(0)

            if type_ in DatetimeConstants.DATE:
                if type_ == DatetimeConstants.DAYS:
                    date.days = number
                elif type_ == DatetimeConstants.WEEKS:
                    date.weeks = number
                elif type_ == DatetimeConstants.MONTHS:
                    date.months = number
                elif type_ == DatetimeConstants.YEARS:
                    date.years = number
            elif type_ in DatetimeConstants.TIME:
                if type_ == DatetimeConstants.SECONDS:
                    time.seconds = number
                elif type_ == DatetimeConstants.MINUTES:
                    time.minutes = number
                elif type_ == DatetimeConstants.HOURS:
                    time.hours = number

        return Method.RELATIVE_DATETIMES, [date, time]

    def parse(self):
        """
        first, check absolute

        check default date formats
        yyyy.mm.dd ...

        check preposition with 'of', 'after', 'before'
        3rd week of august
        3 months 1 day 2 minutes before the fifth week of august
        <relative> <preposition> <absolute>

        check constants
        christmas
        next christmas
        christmas 2024
        :return:
        """

        PROCEDURE = [
            self.parse_absolute_date_formats,
            lambda: self.parse_relative_datetimes(self.string),
            self.parse_constants,
            self.parse_absolute_prepositions
        ]

        result = None

        for part in PROCEDURE:
            if result is None:
                result = part()
            else:
                break

        return result
