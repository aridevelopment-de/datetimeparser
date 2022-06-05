import string as string_utils

from .parsermethods import (
    AbsoluteDateFormatsParser,
    RelativeDatetimesParser,
    ConstantsParser,
    ConstantRelativeExtensionsParser,
    DatetimeDeltaConstantsParser,
    AbsolutePrepositionParser
)


class Parser:
    PROCEDURE = (
        AbsoluteDateFormatsParser().parse,
        RelativeDatetimesParser().parse,
        ConstantsParser().parse,
        ConstantRelativeExtensionsParser().parse,
        DatetimeDeltaConstantsParser().parse,
        AbsolutePrepositionParser().parse
    )

    def __init__(self, string):
        self.string = self.remove_non_ascii(" ".join(string.split()))

    @staticmethod
    def remove_non_ascii(string):
        return ''.join(c for c in string if c in string_utils.printable)

    def parse(self):
        result = None

        for method in self.PROCEDURE:
            if result is None:
                result = method(self.string)
            else:
                break

        return result
