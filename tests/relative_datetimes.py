def run():
    try:
        from datetimeparser.Parser import Parser
        from Colors import Colors
    except ImportError:
        import sys
        sys.path.insert(0, "..")

        from datetimeparser.Parser import Parser
        from Colors import Colors

    test_cases = [
        "in 1Y 2m 3W 3d 5H 6M 7S",
        "in 1 Year 2 months 3 weeks 4 days 5 hours 6 minutes 7 seconds",
        "in a year and in 2 months, in 3 seconds and 4 days",
        "for a year",
        "for 2 days and 1 year",
        "1 year 10 seconds",
        "two years 3 minutes and 1 hour"
    ]

    for testcase in test_cases:
        p = Parser(testcase)
        parser_result = p.parse()

        print(Colors.ANSI_GREEN + "Testcase:", Colors.ANSI_CYAN + testcase + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Parser:", Colors.ANSI_YELLOW + str(parser_result) + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Evaluator:", Colors.ANSI_YELLOW + str(None) + Colors.ANSI_RESET)
        print(Colors.ANSI_BLUE + ("=" * 50))
        print()


if __name__ == '__main__':
    run()