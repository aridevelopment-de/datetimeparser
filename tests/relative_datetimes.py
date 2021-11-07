try:
    from datetimeparser.Parser import Parser
except ImportError:
    import sys
    sys.path.insert(0, "..")

    from datetimeparser.Parser import Parser

test_cases = [
    "in 1Y 2m 3W 3d 5H 6M 7S",
    "in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds",
    "in a year and in 2 months, in 3 seconds and 4 days",
    "for a year",
    "for 2 days and 1 year"
]

for testcase in test_cases:
    p = Parser(testcase)
    parser_result = p.parse()

    print("Testcase:", testcase)
    print("Parser:", parser_result)
    print("Evaluator:", None)
    print("="*10)
    print()
