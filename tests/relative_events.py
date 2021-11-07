def run():
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
        "next 2 years",
        "last month",
        "last 4 years",
        "next three months"
    ]

    for testcase in test_cases:
        p = Parser(testcase)
        parser_result = p.parse()

        print("Testcase:", testcase)
        print("Parser:", parser_result)
        print("Evaluator:", None)
        print("=" * 10)
        print()
