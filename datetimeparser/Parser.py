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

        string = string.split()

        if len(string) == 1:
            # 1st, first, 1.

            string = string[0].strip()

            # check the first tenth numbers
            for kw in NumberCountConstants.ALL:
                for alias in kw.get_all():
                    if alias == string:
                        return (kw.value,)

            # now do manually checks
            # 3th
            if string.endswith("th"):
                if string[:-2].isnumeric():
                    return (int(string[:-2]),)

            # 3.
            if string.endswith("."):
                if string[:-1].isnumeric():
                    return (int(string[:-1]),)

            # 3
            if string.strip().isnumeric():
                return (int(string.strip()),)

            raise ValueError(f'{string} is not a valid number')

        else:
            # second day, 3rd week, 4. month, three months, 3 months
            # special case: the fifth week

            if string[0].strip().lower() == "the":
                string = string[1:]

            if len(string) > 2:
                raise ValueError(f'Too many values to unpack ({string})')

            number, value = string
            number = self.__parse_relative_statement(number)[0]

            ALL = [*Constants.ALL, *MonthConstants.ALL, *WeekdayConstants.ALL, *DatetimeConstants.ALL]

            for kw in ALL:
                if value.strip().lower() in [alias for alias in kw.get_all()]:
                    return number, kw

        raise ValueError(f'Unknown string {string}')

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
            return self.__convert_absolute_preposition_tokens(data)
        return data

    def __convert_absolute_preposition_tokens(self, data):
        new_data = []

        for part in data:
            if part['type'] == 'relative':
                for d in self.__parse_relative_statement(part['data']):
                    new_data.append(d)
            elif part['type'] == 'keyword':
                new_data.append(self.__parse_absolute_keyword(part['data']))
            elif part['type'] == 'absolute':
                for d in self.__parse_absolute_statement(part['data']):
                    new_data.append(d)

        return new_data

    def parse_absolute_prepositions(self):
        splitted = self.__get_absolute_preposition_parts(self.string)

        if splitted is None:
            return None

        tokens = self.__convert_absolute_preposition_tokens(splitted)

        return tokens

    def parse_constants(self):
        # It's important that WeekdayConstant goes before DatetimeConstants because `friday` contains the word `day`
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
                            # next [day] [friday]
                            # next 2 days
                            # next two years
                            # last 2 years

                            preposition = data[0]
                            number = None

                            if len(data[0].split()) > 1:
                                preposition, number = data[0].split()

                                if number.isnumeric():
                                    number = int(number)
                                else:
                                    for n in NumberConstants.ALL:
                                        for number_keyword in n.get_all():
                                            if number in number_keyword:
                                                number = n.value
                                                break
                                        else:
                                            continue

                                        break
                                    else:
                                        raise ValueError(f"Value '{number}' in context '{preposition} {number} {kw}' is not a number")

                                if preposition == "last":
                                    number *= -1
                            else:
                                number = int(preposition.strip().lower() == "next")

                            if keyword in DatetimeConstants.ALL:
                                if keyword in DatetimeConstants.TIME:
                                    return RelativeTime.from_keyword(keyword, delta=number)
                                elif keyword in DatetimeConstants.DATE:
                                    return RelativeDate.from_keyword(keyword, delta=number)
                            elif keyword in WeekdayConstants.ALL:
                                return keyword

                        elif data[1]:
                            # currently only year
                            # xmas 2025

                            if data[1].strip().isnumeric():
                                year = int(data[1])

                                if 1970 <= year <= 9999:
                                    return [keyword, AbsoluteDateTime(year=year)]

                        return

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
