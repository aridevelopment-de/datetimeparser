try:
    from datetimeparser.Parser import Parser
except ImportError:
    import sys
    sys.path.insert(0, "..")

    from datetimeparser.Parser import Parser

test_cases = [
    "second day after christmas",
    "3rd week of august",
    "4. week of august",
    "1st of august",
    "fifth month of 2021",
    "second day after august",
    "3 months before the fifth week of august"
]

for testcase in test_cases:
    p = Parser(testcase)
    parser_result = p.parse()

    print("Testcase:", testcase)
    print("Parser:", parser_result)
    print("Evaluator:", None)
    print("=" * 10)
    print()
