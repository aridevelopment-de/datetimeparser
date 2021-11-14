try:
    from datetimeparser.Parser import Parser
    from datetimeparser.Evaluator import Evaluator
except (ImportError, ModuleNotFoundError):
    import sys
    sys.path.insert(0, '..')

    from datetimeparser.Parser import Parser
    from datetimeparser.Evaluator import Evaluator

from Colors import Colors

class TestValidator:
    def __init__(self, test_cases, real_cases):
        self.test_cases = test_cases
        self.real_cases = real_cases

    def validate(self):
        for testcase in self.test_cases:
            print(Colors.ANSI_GREEN + "Testcase:", Colors.ANSI_CYAN + testcase + Colors.ANSI_RESET)

            p = Parser(testcase)
            parser_result = p.parse()

            print(Colors.ANSI_GREEN + "Parser:", (Colors.ANSI_YELLOW if parser_result is not None else Colors.ANSI_RED) + str(parser_result) + Colors.ANSI_RESET)

            e = Evaluator(parser_result)
            evaluator_result = e.evaluate()

            print(Colors.ANSI_GREEN + "Evaluator:", (Colors.ANSI_YELLOW if evaluator_result is not None else Colors.ANSI_RED) + str(evaluator_result) + Colors.ANSI_RESET)
            print(Colors.ANSI_BLUE + ("=" * 80) + Colors.ANSI_RESET)
            print()