try:
    from datetimeparser.Parser import Parser
except ImportError:
    import sys
    sys.path.insert(0, "..")

    from datetimeparser.Parser import Parser

test_cases = [
    "next christmas",
    "christmas",
    "new years eve",
    "xmas 2025",
    "eastern 2010",
    "next second",
    "next hour",
    "next year",
    "next friday",
    "next 2 years"
]

for testcase in test_cases[-1:]:
    p = Parser(testcase)
    result = p.parse()

    print("Testcase:", testcase)
    print(result)
    print()
