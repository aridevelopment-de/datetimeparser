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

    for testcase in test_cases[:1]:
        p = Parser(testcase)
        parser_result = p.parse()

        print(Colors.ANSI_GREEN + "Testcase:", Colors.ANSI_CYAN + testcase + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Parser:", Colors.ANSI_YELLOW + str(parser_result) + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Evaluator:", Colors.ANSI_YELLOW + str(None) + Colors.ANSI_RESET)
        print(Colors.ANSI_BLUE + ("=" * 50))
        print()


if __name__ == '__main__':
    run()