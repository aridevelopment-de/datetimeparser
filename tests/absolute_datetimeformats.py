def run():
    try:
        from datetimeparser.Parser import Parser
        from datetimeparser.Evaluater import Evaluator
    except ImportError:
        import sys
        sys.path.insert(0, "..")

        from datetimeparser.Parser import Parser
        from datetimeparser.Evaluater import Evaluator

    test_cases = [
        "2017.08.03 03:04:05",
        "05.05.2017 03:04:10",
        "10.01.2022",
        "2023.01.10",
        "03:02:10",
        "01.01.2023 05:03",
        "07:16",
        "08:20"
    ]

    for testcase in test_cases:
        p = Parser(testcase)
        parser_result = p.parse()

        e = Evaluator(parser_result)
        evaluator_result = e.evaluate()

        print("Testcase:", testcase)
        print("Parser:", parser_result)
        print("Evaluator:", evaluator_result)
        print("=" * 10)
        print()
  
