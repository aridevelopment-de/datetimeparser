from json import dumps

from datetimeparser.Parser import Parser

test_cases = [
    "3rd week of august",
    "4. week of august",
    "1st of august",
    "fifth month of 2021",
    "second day after august",
    "3 months before the fifth week of august"
]

for testcase in test_cases:
    p = Parser(testcase)
    result = p.parse()

    print("Testcase:", testcase)
    print(result)
    print()