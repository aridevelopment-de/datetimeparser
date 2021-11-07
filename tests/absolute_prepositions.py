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

        print(Colors.ANSI_GREEN + "Testcase:", Colors.ANSI_YELLOW + testcase + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Parser:", Colors.ANSI_YELLOW + str(parser_result) + Colors.ANSI_RESET)
        print(Colors.ANSI_GREEN + "Evaluator:", Colors.ANSI_YELLOW + str(None) + Colors.ANSI_RESET)
        print(Colors.ANSI_BLUE + ("=" * 50))
        print()
