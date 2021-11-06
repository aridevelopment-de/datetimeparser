try:
    from datetimeparser.Parser import Parser
except ImportError:
    import sys
    sys.path.insert(0, "..")

    from datetimeparser.Parser import Parser

test_cases = [
    "2017.08.03 03:04:05",
    "05.05.2017 03:04:10",
    "10.01.2022",
    "2023.01.10",
    "03:02:10",
    "01.01.2023 05:03",
    "07:16"
]

for testcase in test_cases:
    p = Parser(testcase)
    result = p.parse()

    print("Testcase:", testcase)
    print(result)
    print()