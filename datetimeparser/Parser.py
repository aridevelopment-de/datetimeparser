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
        else:
            absolute = (absolute,)

        return {'type': 'relative', 'data': relative}, \
               {'type': 'keyword', 'data': word}, \
               {'type': 'absolute', 'data': absolute}

    def parse_relative_statement(self, string):
        return string

    def parse_absolute_keyword(self, string):
        return string

    def parse_absolute_statement(self, data):
        return data

    def convert_absolute_preposition_tokens(self, data):
        new_data = []

        for part in data:
            if part['type'] == 'relative':
                new_data.append(self.parse_relative_statement(part['data']))
            elif part['type'] == 'keyword':
                new_data.append(self.parse_absolute_keyword(part['data']))
            elif part['type'] == 'absolute':
                new_data.append(self.parse_absolute_statement(part['data']))

        return new_data

    def parse_absolute_prepositions(self):
        splitted = self.get_absolute_preposition_parts(self.string)
        # tokens = self.convert_absolute_preposition_tokens(splitted)

        return splitted

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
            # self.parse_absolute_date_formats,
            self.parse_absolute_prepositions
        ]

        result = None

        for part in PROCEDURE:
            if result is None:
                result = part()
            else:
                break

        return result