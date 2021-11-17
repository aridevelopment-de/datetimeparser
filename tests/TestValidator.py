import time

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
        failed = []

        for i, testcase in enumerate(self.test_cases):
            print(Colors.ANSI_GREEN + "Testcase:", Colors.ANSI_CYAN + testcase + Colors.ANSI_RESET)

            p = Parser(testcase)
            parser_result = p.parse()

            time.sleep(.1)

            print(Colors.ANSI_GREEN + "Parser:", (Colors.ANSI_YELLOW if parser_result is not None else Colors.ANSI_RED) + str(parser_result) + Colors.ANSI_RESET)

            e = Evaluator(parser_result)
            evaluator_result = e.evaluate()

            time.sleep(.1)

            print(Colors.ANSI_GREEN + "Evaluator:", (Colors.ANSI_PURPLE if evaluator_result is not None else Colors.ANSI_RED) + str(evaluator_result) + Colors.ANSI_RESET)
            print()

            if i < len(self.real_cases):
                test_success = evaluator_result == self.real_cases[i]

                if not test_success:
                    failed.append(testcase)

                print(Colors.ANSI_BLUE + "Expected:", Colors.ANSI_CYAN + str(self.real_cases[i]) + Colors.ANSI_RESET)
                print(Colors.ANSI_BLUE + "Success?:", (Colors.ANSI_GREEN if test_success else Colors.ANSI_RED) + str(test_success) + Colors.ANSI_RESET)
                print()

            print(Colors.ANSI_BLUE + ("=" * 80) + Colors.ANSI_RESET)
            print()

        return failed, len(self.test_cases)