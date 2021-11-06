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

                return timings
            except ValueError:
                continue

        return None

    def get_absolute_preposition_parts(self, string):
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

        if self.get_absolute_preposition_parts(absolute) is not None:
            absolute = self.get_absolute_preposition_parts(absolute)

        return {'type': 'relative', 'data': relative}, \
               {'type': 'keyword', 'data': word}, \
               {'type': 'absolute', 'data': absolute}

    def parse_relative_statement(self, string):
        """
        TODO: Use the parser for the whole relative part
        :param string:
        :return:
        """
        return string

    def parse_absolute_keyword(self, string):
        string = string.lower()

        for pr in self.ABSOLUTE_PREPOSITION_TOKENS:
            for kw in pr.get_all():
                if string == kw:
                    return pr

        raise ValueError('no preposition given')

    def parse_absolute_statement(self, data):
        if isinstance(data, str):
            """
            Constants
            Years
            Months
            Weekdays
            """

            data = data.lower()
            keywords = [*Constants.ALL, *MonthConstants.ALL]

            for keyword in keywords:
                if data in [kw for kw in keyword.get_all()]:
                    return (keyword,)
                elif data.isnumeric():
                    data = int(data)

                    if 1970 <= data <= 9999:
                        return (AbsoluteDateTime(year=data),)
        else:
            return self.convert_absolute_preposition_tokens(data)
        return data

    def convert_absolute_preposition_tokens(self, data):
        new_data = []

        for part in data:
            if part['type'] == 'relative':
                new_data.append(self.parse_relative_statement(part['data']))
            elif part['type'] == 'keyword':
                new_data.append(self.parse_absolute_keyword(part['data']))
            elif part['type'] == 'absolute':
                for d in self.parse_absolute_statement(part['data']):
                    new_data.append(d)

        return new_data

    def parse_absolute_prepositions(self):
        splitted = self.get_absolute_preposition_parts(self.string)

        if splitted is None:
            return None

        tokens = self.convert_absolute_preposition_tokens(splitted)

        return tokens

    def parse_constants(self):
        keywords = [*Constants.ALL, *MonthConstants.ALL, *WeekdayConstants.ALL, *DatetimeConstants.ALL]

        for keyword in keywords:
            if self.string.lower() in [kw for kw in keyword.get_all()]:
                return [keyword]
            else:
                for kw in keyword.get_all():
                    if kw in self.string.lower():
                        data = self.string.split(kw)

                        if data[0]:
                            # preposition
                            # next

                            if keyword in DatetimeConstants.ALL:
                                if keyword in DatetimeConstants.TIME:
                                    return RelativeTime.from_keyword(keyword, delta=data[0].lower() == "next")
                                elif keyword in DatetimeConstants.DATE:
                                    return RelativeDate.from_keyword(keyword, delta=data[0].lower() == "next")

                        elif data[1]:
                            # currently only year
                            # xmas 2025

                            if data[1].strip().isnumeric():
                                year = int(data[1])

                                if 1970 <= year <= 9999:
                                    return [keyword, AbsoluteDateTime(year=year)]
                        break

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
            self.parse_absolute_prepositions,
            self.parse_constants
        ]

        result = None

        for part in PROCEDURE:
            if result is None:
                result = part()
            else:
                break

        return result