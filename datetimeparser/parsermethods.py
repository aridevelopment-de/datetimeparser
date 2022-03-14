import re
from typing import Optional, Tuple, Union

from .enums import *
from .baseclasses import *


class RelativeDatetimeHelper:
    @staticmethod
    def from_keyword(keyword: Constant, delta: int = 1) -> RelativeDateTime:
        if keyword == DatetimeConstants.DAYS:
            return RelativeDateTime(days=delta)
        elif keyword == DatetimeConstants.WEEKS:
            return RelativeDateTime(weeks=delta)
        elif keyword == DatetimeConstants.MONTHS:
            return RelativeDateTime(months=delta)
        elif keyword == DatetimeConstants.YEARS:
            return RelativeDateTime(years=delta)
        elif keyword == DatetimeConstants.HOURS:
            return RelativeDateTime(hours=delta)
        elif keyword == DatetimeConstants.MINUTES:
            return RelativeDateTime(minutes=delta)
        elif keyword == DatetimeConstants.SECONDS:
            return RelativeDateTime(seconds=delta)


class AbsoluteDateFormatsParser:
    DATETIME_FORMATS = (
        "%Y.%m.%d %H:%M:%S",
        "%d.%m.%Y %H:%M:%S",
        "%Y.%m.%d",
        "%d.%m.%Y",
        "%H:%M:%S",
        "%H:%M",
        "%Y.%m.d %H:%M",
        "%d.%m.%Y %H:%M"
    )

    CLOCKTIME_FORMATS = (
        "%H:%M:%S",
        "%H:%M"
    )

    def parse(self, string: str) -> Union[None, Tuple[MethodEnum, AbsoluteDateTime]]:
        """
        Parses strings like "2020.01.01 12:00:00" or "2020.01.01"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the parsed data or None
        """
        for datetime_format in self.DATETIME_FORMATS:
            # Trying to find the right datetime format
            # And then instantly return the parsed datetime
            try:
                time = datetime.strptime(string, datetime_format)
            except ValueError:
                continue

            resulting_datetime = AbsoluteDateTime(hour=time.hour, minute=time.minute, second=time.second)

            if datetime_format not in self.CLOCKTIME_FORMATS:
                resulting_datetime.year = time.year
                resulting_datetime.month = time.month
                resulting_datetime.day = time.day

            return Method.ABSOLUTE_DATE_FORMATS, resulting_datetime

        return None


class RelativeDatetimesParser:
    PREPOSITIONS = ("in", "for", "next", "last")
    SKIPPABLE_KEYWORDS = ("and", "in", "for", ",")

    def parse(self, string: str) -> Union[None, Tuple[MethodEnum, RelativeDateTime]]:  # noqa: C901
        """
        Parses strings like "in 5 days" or "in 5 days and 3 hours"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the parsed data or None
        """

        # Checks if the string starts with a preposition
        # And then cuts it off because we need the preposition to differentiate future and past events
        for preposition in self.PREPOSITIONS:
            if string.startswith(preposition):
                string = string[len(preposition):]
                break
        else:
            preposition = ""

        new_data = []

        for argument in string.split():
            not_possible = True
            argument = argument.lower()

            # Skip unnecessary keywords
            if argument.lower() in self.SKIPPABLE_KEYWORDS:
                continue

            # an `a` always represents a 1 (e.g. a day = 1 day)
            elif argument.lower() == "a":
                new_data.append(1 if preposition != "last" else -1)
                not_possible = False

            # Cut off commas, they get in the way with parsing
            elif argument.endswith(","):
                argument = argument[:-1]

            # If the argument is a mini date format (m = minutes, s = seconds, ...) add the corresponding keyword to the list
            # Prepends a 1 if there wasn't a number set before the keyword (e.g. "s" doesnt make any sense so we prepend it with a 1)
            if len(argument) == 1:
                keyword = DatetimeConstants.convert_from_mini_date(argument)

                if keyword is not None:
                    if not new_data:
                        # If there is no number before the keyword, we need to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)
                    elif not isinstance(new_data[-1], int):
                        # If the element before the keyword is not a number we have to add one ourselves
                        # This occurs when TODO
                        new_data.append(1 if preposition != "last" else -1)

                    new_data.append(keyword)
                    not_possible = False

            # If the argument is a number, simply add it to the list
            if argument.isnumeric():
                new_data.append(int(argument) if preposition != "last" else -int(argument))
                not_possible = False

            # If the argument represents a number (e.g. "one", "two", ...) simply add their integer value to the list
            for kw in NumberConstants.ALL:
                if argument.lower() in kw.get_all():
                    new_data.append(kw.value)
                    not_possible = False
                    break

            # If the argument is a datetime keyword (e.g. "year", "month", ...) add the keyword to the list
            # Prepends a 1 if there wasn't a number set before the keyword (e.g. "months" doesnt make any sense so we prepend it with a 1)
            for keyword in DatetimeConstants.ALL:
                if argument.lower() in keyword.get_all():
                    if not new_data:
                        # If there is no number before the keyword, we need to add one ourselves
                        new_data.append(1 if preposition != "last" else -1)
                    elif not isinstance(new_data[-1], int):
                        # If the element before the keyword is not a number we have to add one ourselves
                        # This occurs when TODO
                        new_data.append(1 if preposition != "last" else -1)

                    new_data.append(keyword)
                    not_possible = False
                    break
            else:
                # If the everything up to the last letter is numeric and the last letter is a valid mini date keyword (e.g. "30d", "10m", ...)
                # Add the number to the list and add the keyword to the list
                if argument[:-1].isnumeric():
                    number = int(argument[:-1]) if preposition != "last" else -int(argument[:-1])
                    keyword = argument[-1]

                    keyword = DatetimeConstants.convert_from_mini_date(keyword)

                    if keyword is not None:
                        new_data.append(number)
                        new_data.append(keyword)

                        not_possible = False

            # If none of the above if cases could find any data
            # Then we might've just encountered an invalid string
            # And other parsing methods might be able to parse it
            if not_possible:
                return None

        date = RelativeDateTime()

        # Has to be a multiple of 2 (because there's always a number before a keyword e.g. "1 day")
        # Otherwise it's not a valid relative date
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
                    date.seconds = number
                elif type_ == DatetimeConstants.MINUTES:
                    date.minutes = number
                elif type_ == DatetimeConstants.HOURS:
                    date.hours = number

        return Method.RELATIVE_DATETIMES, date


class ConstantsParser:
    # Weekday must go before DatetimeConstants because `friday` contains the word `day`
    CONSTANT_KEYWORDS = (*DatetimeDeltaConstants.ALL, *Constants.ALL, *MonthConstants.ALL, *WeekdayConstants.ALL, *DatetimeConstants.ALL)
    PREPOSITIONS = ("last", "next", "this", "previous", "at")
    PAST_PREPOSITIONS = ("last", "previous")
    FUTURE_PREPOSITIONS = ("next", "this")

    # Order is important because "at" and "the" are both in "at the"
    CUTOFF_KEYWORDS = ("at the", "in the", "at", "the")

    def _find_constant(self, argument: str) -> Optional[Constant]:
        """
        Finds a constant without any preposition or years
        Simply just "today" or "christmas"

        :param argument: The argument to look for
        :return: The constant if found, None otherwise
        """

        for keyword in self.CONSTANT_KEYWORDS:
            if argument in keyword.get_all():
                return keyword

        return None

    def parse(self, string: str) -> Optional[Tuple[MethodEnum, Tuple]]:  # noqa: C901
        """
        Parses strings like "today" or "next christmas" or "christmas 2022" or "last christmas"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the data or None
        """
        string = string.lower()

        # Cut off 'at', 'at the' and 'the'
        for cutoff_word in self.CUTOFF_KEYWORDS:
            if string.startswith(cutoff_word):
                string = string[len(cutoff_word):]

        # Strip whitespace
        string = " ".join(string.split())

        # Cut off the preposition if the strings starts with one and save the preposition
        # To differentiate future and past
        for preposition in self.PREPOSITIONS:
            if string.startswith(preposition):
                string = string[len(preposition):]
                break
        else:
            preposition = None

        string = " ".join(string.split())

        arguments = string.split()

        # If the last argument is a number, it must be a year
        # e.g. "christmas 2024"
        if arguments[-1].isnumeric():
            year = int(arguments.pop(-1))
            constant = self._find_constant(" ".join(arguments))

            if constant is None:
                return None
            else:
                return Method.CONSTANTS, (constant, AbsoluteDateTime(year=year))
        else:
            # Otherwise search for constants with or without prepositions
            # e.g. "christmas", "tomorrow", "tuesday"
            constant = self._find_constant(string)

            if constant is None:
                return None
            else:
                if preposition is None:
                    return Method.CONSTANTS, (constant,)
                else:
                    # Depending on the preposition the constant is either a future or past constant
                    if preposition in self.PAST_PREPOSITIONS:
                        return Method.CONSTANTS, (constant, RelativeDateTime(days=-1))
                    elif preposition in self.FUTURE_PREPOSITIONS:
                        if constant in DatetimeConstants.ALL:
                            if constant in DatetimeConstants.TIME:
                                return Method.CONSTANTS, (RelativeDatetimeHelper.from_keyword(constant, delta=1),)
                            elif constant in DatetimeConstants.DATE:
                                return Method.CONSTANTS, (RelativeDatetimeHelper.from_keyword(constant, delta=1),)
                        elif constant in [*WeekdayConstants.ALL, *Constants.ALL]:
                            return Method.CONSTANTS, (constant,)
                        else:
                            return None

        return None


class ConstantRelativeExtensionsParser:
    ABSOLUTE_KEYWORDS = (*Constants.ALL, *WeekdayConstants.ALL, *MonthConstants.ALL)
    RELATIVE_KEYWORDS = (*DatetimeDeltaConstants.ALL,)
    RELATIVE_TYPES = (RelativeDateTime,)
    CONSTANT_KEYWORDS = ABSOLUTE_KEYWORDS + RELATIVE_KEYWORDS

    PREPOSITIONS = ("last", "next", "this", "previous", "at", "on", "in")
    PAST_PREPOSITIONS = ("last", "previous")
    FUTURE_PREPOSITIONS = ("next", "this", "in")
    DATETIME_PREPOSITIONS = ("at", "on")

    # Order is important because "at" and "the" are both in "at the"
    CUTOFF_KEYWORDS = ("at the", "at", "the")

    @staticmethod
    def _find_number(string: str) -> Optional[int]:
        """
        Searches for a number in the string

        :param string: The string to search in
        :return: The number if found, None otherwise
        """

        if string == "a":
            return 1

        if string.isdecimal():
            return int(string)

        for constant in NumberConstants.ALL:
            for alias in constant.get_all():
                if string == alias:
                    return constant.value

        return None

    @staticmethod
    def _find_datetime_constant(string: str) -> Optional[Constant]:
        """
        Searches for a datetime constant in the string

        :param string: The string to search in
        :return: The constant if found, None otherwise
        """

        for constant in DatetimeConstants.ALL:
            for alias in constant.get_all():
                if string == alias:
                    return constant

        return None

    def _find_constant(self, argument: str) -> Optional[Constant]:
        """
        Finds a constant without any preposition or years
        Simply just "tomorrow" or "daylight change"

        :param argument: The argument to look for
        :return: The constant if found, None otherwise
        """

        for keyword in self.CONSTANT_KEYWORDS:
            if argument in keyword.get_all():
                return keyword

        return None

    def _get_preposition(self, string: str) -> Optional[Tuple[str, str]]:
        """
        Gets the preposition of a string if it exists (e.g. "next)
        :param string: the current string
        :return: the preposition if it exists otherwise None and the new string
        """
        string = " ".join(string.split())

        # Cut off the preposition if the strings starts with one and save the preposition
        # To differentiate future and past
        for preposition in self.PREPOSITIONS:
            if string.startswith(preposition):
                string = string[len(preposition):]
                break
        else:
            preposition = "at"

        string = " ".join(string.split())

        return preposition, string

    def _get_preposition_keyword(self, string: str) -> Optional[Tuple[str, str, Union[Constant, RelativeDateTime], str]]:
        """
        Gets the preposition and the constant of a string if it exists (e.g. "next daylight change)
        :param string: the current string
        :return: the preposition, the keyword as the string, the keyword and the new string if found otherwise None
        """
        # Cut off 'at', 'at the' and 'the'
        for cutoff_word in self.CUTOFF_KEYWORDS:
            if string.startswith(cutoff_word):
                string = string[len(cutoff_word):]
                string = string.strip()

        preposition, string = self._get_preposition(string)

        # "Bruteforce" the next arguments
        # Until a keyword has been found
        # The keyword can either be a constant, an absolute time, a clock time or a constant with a number
        # Unfortunately, we have to implement such parsing methods ourselves because we cannot use other parsers
        arguments = string.split()

        for i in range(1, len(arguments) + 1):
            tryable_keyword = " ".join(arguments[:i])

            # Try general keywords (e.g. "afternoon", "tomorrow", ...)
            # TODO: Add support for years (e.g. "monday 2021")
            keyword = self._find_constant(tryable_keyword)

            if keyword is not None:
                break

            # Try datetime delta constants (e.g. "17pm", "17:30", ...)
            datetime_delta_constants_parser = DatetimeDeltaConstantsParser()
            keyword = datetime_delta_constants_parser.parse(tryable_keyword)

            if keyword is not None:
                keyword = keyword[1]

                if preposition in self.DATETIME_PREPOSITIONS:
                    break
                else:
                    continue

            # Try absolute datetime formats (e.g. "17:30", "01.02.2020", ...)
            absolute_datetime_parser = AbsoluteDateFormatsParser()
            absolute_datetime_parser.DATETIME_FORMATS = (
                "%d.%m.%Y",
                "%Y.%m.%d"
            )
            absolute_datetime_parser.CLOCKTIME_FORMATS = ()
            keyword = absolute_datetime_parser.parse(tryable_keyword)

            if keyword is not None:
                keyword = keyword[1]

                if preposition in self.DATETIME_PREPOSITIONS:
                    break
                else:
                    return None

            # Try a mix of numbers and constants (e.g. "two weeks", "two years", ...)
            # TODO: This is the second only case where years could also be included
            # e.g. "(monday in) two weeks 2020"
            if len(tryable_keyword.split()) >= 2:
                number = self._find_number(tryable_keyword.split()[0])

                if number is None:
                    continue

                datetime_constant = self._find_datetime_constant(" ".join(tryable_keyword.split()[1:]))

                if datetime_constant is None:
                    continue

                keyword = RelativeDatetimeHelper.from_keyword(datetime_constant, delta=number)
                break
        else:
            return None

        return preposition, tryable_keyword, keyword, string

    def parse(self, string: str) -> Optional[Tuple[Method, Tuple]]:
        """
        Parses strings like "tomorrow afternoon" or "daylight change yesterday" or "monday in two weeks" or "tomorrow at 17"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the data or None
        """
        string = string.lower()
        result = self._get_preposition_keyword(string)

        if result is None:
            return None

        first_preposition, tryable_keyword, first_keyword, string = result
        string = string[len(tryable_keyword):]
        string = " ".join(string.split())

        # There has to be some contents left
        # Otherwise its not valid
        if not string:
            return None

        result = self._get_preposition_keyword(string)

        if result is None:
            return None

        second_preposition, tryable_keyword, second_keyword, string = result

        if first_keyword in self.ABSOLUTE_KEYWORDS and second_keyword in self.ABSOLUTE_KEYWORDS:
            return None

        if first_keyword in self.RELATIVE_KEYWORDS and second_keyword in self.RELATIVE_KEYWORDS:
            return None

        if first_keyword in self.RELATIVE_TYPES and second_keyword in self.RELATIVE_TYPES:
            return None

        if first_keyword in self.RELATIVE_KEYWORDS or type(second_keyword) in self.RELATIVE_TYPES:
            relative = first_preposition, first_keyword
            absolute = second_preposition, second_keyword
        else:
            relative = second_preposition, second_keyword
            absolute = first_preposition, first_keyword

        return Method.CONSTANTS_RELATIVE_EXTENSIONS, (*relative, *absolute)


class DatetimeDeltaConstantsParser:
    DATETIME_DELTA_CONSTANTS_PATTERN = re.compile("(([0-9]{1,2}:[0-9]{1,2})|([0-9]{1,2}))(am|pm|h| o\'clock|)")
    CLOCKTIME_FORMATS = (
        "%H:%M:%S",
        "%H:%M"
    )

    def parse(self, string: str) -> Optional[Tuple[MethodEnum, RelativeDateTime]]:  # noqa: C901
        """
        Parses strings like "at 3pm tomorrow" or "at 1am" or "at 10:30" or "at 17"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the data or None
        """

        data = string.split()

        if data[0] == "at":
            data.pop(0)

        if not data:
            return None

        # Matches the time and optional am/pm
        if self.DATETIME_DELTA_CONSTANTS_PATTERN.match(data[0]):
            time = data.pop(0)
            after_midday = time.endswith("pm") if time.endswith(("pm", "am")) else None
            time = time.replace("pm", "").replace("am", "").replace("h", "").replace(" o'clock", "")
            parsed_time = None

            for clocktime_format in self.CLOCKTIME_FORMATS:
                try:
                    parsed_time = datetime.strptime(time, clocktime_format)
                except ValueError:
                    continue

            # If the time does not match a clocktime format, does not contain a colon and is a number
            # e.g. "3(pm|am)", return that time respecting the after_midday flag
            if not parsed_time and time.count(":") == 0 and time.isdigit():
                if after_midday is not None:
                    parsed_time = RelativeDateTime(hours=(12 if after_midday else 0) + int(time))
                else:
                    parsed_time = RelativeDateTime(hours=int(time))
            elif parsed_time:
                if after_midday is not None:
                    parsed_time = RelativeDateTime(hours=(12 if after_midday else 0) + parsed_time.hour, minutes=parsed_time.minute, seconds=parsed_time.second)
                else:
                    parsed_time = RelativeDateTime(hours=parsed_time.hour, minutes=parsed_time.minute, seconds=parsed_time.second)
            else:
                return None

            # If the time is invalid return None
            if parsed_time.hours > 23 or parsed_time.minutes > 59 or parsed_time.seconds > 59:
                return None

            # If there's no more content left
            # Return the parsed time
            if not data:
                return Method.DATETIME_DELTA_CONSTANTS, parsed_time
            else:
                # Otherwise search for constants like
                # "at 3 in the morning"
                # "at 3 in the afternoon"

                rest = " ".join(data)

                # Find the matching keyword
                for kw in DatetimeDeltaConstants.ALL:
                    for alias in kw.get_all():
                        if rest in ("in the " + alias, alias):
                            value = kw.value
                            break
                    else:
                        continue

                    break
                else:
                    return None

                # "at 3pm in the morning" contains pm and in the morning
                # Is not valid so we return None
                if after_midday is not None:
                    return None

                # Value is either 0 or 12 (depending on the constant)
                parsed_time.hours += value

                # If the time is invalid return None
                if parsed_time.hours > 23:
                    return None

                return Method.DATETIME_DELTA_CONSTANTS, parsed_time

        return None


class AbsolutePrepositionParser:
    ABSOLUTE_PREPOSITION_TOKENS = (
        Keywords.OF,
        Keywords.AFTER,
        Keywords.BEFORE
    )

    RELATIVE_DATA_SKIPPABLE_WORDS = (
        "and",
        ",",
        "the"
    )

    RELATIVE_PAST_PREPOSITIONS = (
        "before"
    )

    MAX_RECURSION_DEPTH = 13

    def _split_data(self, string: str) -> Optional[Tuple[dict, dict, dict]]:
        """
        Splits the data into 3 parts
        The relative part, the keyword and the absolute part
        e.g. "3 months after christmas" -> ("3 months", "after", "christmas")

        :param string: The string to split
        :return: The splitted data or None
        """

        # If none of the known prepositions are in the string, return None
        if not any(absolute_preposition.name in string for absolute_preposition in self.ABSOLUTE_PREPOSITION_TOKENS):
            return None

        word = None
        char_count = 0

        # Count the number of characters up to the preposition in the string
        for word in string.split():
            char_count += len(word) + 1

            if word.lower() in map(lambda absolute_preposition: absolute_preposition.name, self.ABSOLUTE_PREPOSITION_TOKENS):
                break

        # Split the string into the relative part, the keyword and the absolute part
        # Subtract the length of the last word (because it's the preposition) and 2 because we accounted for 2 spaces in the loop
        relative = string[:char_count - len(word) - 2]
        absolute = string[char_count:]

        # There may be more prepositions in the absolute part so we try it again via recursion
        recursion_result = self._split_data(absolute)

        if recursion_result is not None:
            absolute = recursion_result

        return {'type': 'relative', 'data': relative}, {'type': 'keyword', 'data': word}, {'type': 'absolute', 'data': absolute}

    def _parse_relative_statement(self, relative_statement: str) -> List[Union[int, Constant]]:  # noqa: C901
        """
        Parses strings like "3 seconds, 2 minutes and 4 hours", "the fifth day", "4. week"
        It resembles `relative_datetimes`

        :param relative_statement: The statement to parse
        :return: List of integers and keywords
        """

        arguments = relative_statement.lower().split()
        returned_data = []

        for argument in arguments:
            if argument.endswith(","):
                argument = argument[:-1]

            if argument.startswith(","):
                argument = argument[1:]

            # Skip words like "and", "," or "the"
            if argument in self.RELATIVE_DATA_SKIPPABLE_WORDS:
                continue

            # 'a' means the same as '1' (e.g. 'a day' => '1 day')
            if argument == "a":
                returned_data.append(1)
                continue

            if argument.isnumeric():
                returned_data.append(int(argument))
                continue

            found_keyword = False

            # '1st', '1.', 'first', ...
            for keyword in NumberCountConstants.ALL:
                for alias in keyword.get_all():
                    if alias == argument:
                        returned_data.append(keyword.value)
                        found_keyword = True
                        break
                else:
                    continue

                break

            if found_keyword:
                continue

            # 'one', 'two', 'three', ...
            for keyword in NumberConstants.ALL:
                for alias in keyword.get_all():
                    if alias == argument:
                        returned_data.append(keyword.value)
                        found_keyword = True
                        break
                else:
                    continue

                break

            if found_keyword:
                continue

            # 'seconds', 'minutes', 'hours', ...
            for keyword in DatetimeConstants.ALL:
                for alias in keyword.get_all():
                    if alias == argument:
                        returned_data.append(keyword)
                        break
                else:
                    continue

                break

        return returned_data

    def _concatenate_relative_data(self, relative_data_tokens: List[Union[int, Constant]], preposition: str) -> List[Union[int, Constant, RelativeDateTime]]:
        """
        Concatenates [1, RelativeDate(DAY), 2, RelativeDate(MONTH)] into [RelativeDate(days=1, months=2)]
        respecting the preposition (future and past)

        :param relative_data_tokens: The already parsed relative data
        :param preposition: The preposition
        :return: List of Keywords and integers
        """

        # If the data does not divide by 2, we cannot concatenate it
        # e.g. "1st (of july)"
        if len(relative_data_tokens) % 2 != 0:
            return relative_data_tokens

        returned_data = []

        for i in range(0, len(relative_data_tokens), 2):
            value, unit = relative_data_tokens[i], relative_data_tokens[i + 1]

            # We can only concatenate Datetime Constants like 'seconds', 'days', 'months', ...
            if isinstance(value, int) and unit in DatetimeConstants.ALL:
                if preposition in self.RELATIVE_PAST_PREPOSITIONS:
                    value *= -1

                if unit in DatetimeConstants.DATE:
                    current_data = RelativeDatetimeHelper.from_keyword(unit, value)
                elif unit in DatetimeConstants.TIME:
                    current_data = RelativeDatetimeHelper.from_keyword(unit, value)
                else:
                    raise RuntimeError("Unknown Datetime Constant:", unit)

                # We cannot concatenate anything if there's no data
                if i == 0:
                    returned_data.append(current_data)
                else:
                    # Check if the latest entry is the same type as the current unit
                    if isinstance(returned_data[-1], type(current_data)):
                        data_before = returned_data.pop()
                        new_data = data_before.concatenate(data_before, current_data)
                        returned_data.append(new_data)
                    else:
                        # Otherwise we cannot concatenate both parts of the data so we just append the current one
                        returned_data.append(current_data)

        return returned_data

    def _parse_absolute_statement(self, data: Union[str, Tuple]) -> Optional:
        """
        Parses constant values like "christmas", "previous st. patricks day", ..
        If the input is a Tuple containing the absolute preposition tokens, we return the result of`_convert_tokens`
        This happens because strings like "(10 days after) 3 months before christmas" are also valid

        :param data: Either the string to parse or a Tuple containing absolute preposition tokens
        :return: The parsed result (no typing specified because there are just too many values)
        """

        if isinstance(data, str):
            # TODO: Call ConstantRelativeExtensionsParser as well
            constants_parser = ConstantsParser()
            constants_parser.CONSTANT_KEYWORDS = (*Constants.ALL, *MonthConstants.ALL, *WeekdayConstants.ALL)
            constants_parser.PREPOSITIONS = ("last", "next", "this", "previous")
            constants_parser.PAST_PREPOSITIONS = ("last", "previous")
            constants_parser.FUTURE_PREPOSITIONS = ("next", "this")
            constants_parser.CUTOFF_KEYWORDS = ("the",)

            result = constants_parser.parse(data)

            if result is None:
                # If the result is None there may be just a normal year (e.g. "2018")
                if data.isnumeric():
                    return (AbsoluteDateTime(year=int(data)),)
                else:
                    return None
            else:
                # The first element is the Method signature (Method.CONSTANTS)
                return result[1]
        else:
            return self._convert_tokens(data)

    def _convert_tokens(self, tokens: Tuple[dict, dict, dict]) -> Optional[List[Union[int, Constant, RelativeDateTime]]]:
        """
        Converts and parses the splitted tokens from _split_data into Tokens suited for the Evaluator

        :param tokens: Tokens from _split_data
        :return: A List containing numbers and keywords
        """

        returned_data = []

        # Choose the right parsing method for the specific data types
        for i, data_part in enumerate(tokens):
            if data_part["type"] == "relative":
                # "3 hours and 4 minutes (after christmas)", "the 5th (of july)", ...
                relative_data = []

                for relative_part_data in self._parse_relative_statement(data_part["data"]):
                    relative_data.append(relative_part_data)

                preposition = tokens[1]["data"]
                relative_data = self._concatenate_relative_data(relative_data, preposition)

                for relative_part_data in relative_data:
                    returned_data.append(relative_part_data)
            elif data_part["type"] == "keyword":
                # "of", "before", ...
                for keyword in self.ABSOLUTE_PREPOSITION_TOKENS:
                    if keyword.name == data_part["data"]:
                        returned_data.append(keyword)
                        break
                else:
                    raise ValueError("No preposition given")
            elif data_part["type"] == "absolute":
                absolute_data = self._parse_absolute_statement(data_part["data"])

                if absolute_data is None:
                    return None

                for absolute_part_data in absolute_data:
                    returned_data.append(absolute_part_data)

        return returned_data

    def parse(self, string: str) -> Optional[Tuple[MethodEnum, List[Union[int, Constant, RelativeDateTime]]]]:
        """
        Parses strings like "3 days after christmas" or "1 hour, 2 minutes and 5 days after 3 months before christmas"
        Returns None if the string cannot be parsed

        :param string: The string to parse
        :return: A tuple containing the method and the data or None
        """

        prepared_data = self._split_data(string)

        if prepared_data is None:
            return None

        data = self._convert_tokens(prepared_data)

        if data is None:
            return None

        return Method.ABSOLUTE_PREPOSITIONS, data
