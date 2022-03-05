import argparse

try:
    from testcases import testcases
    from colors import Colors

    from datetimeparser.parser import Parser
    from datetimeparser.evaluator import Evaluator
except (ImportError, ModuleNotFoundError):
    import sys

    sys.path.insert(0, "..")

    from testcases import testcases
    from colors import Colors

    from datetimeparser.parser import Parser
    from datetimeparser.evaluator import Evaluator

testcases_to_run: list[str] = []


class StatusType:
    SUCCESS = 0
    PARSER_ERROR = 1
    PARSER_EXCEPTION = 1.5
    EVALUATOR_ERROR = 2
    EVALUATOR_EXCEPTION = 2.5
    WRONG_RESULT = 3
    NO_VALIDATION = 4


def run_testcase(testcase, disable_colored_output=False):
    p = Parser(testcase)
    parser_result = p.parse()

    if parser_result is None:
        if not disable_colored_output:
            return print(f"{Colors.ANSI_RED}{testcase} (❌): {Colors.ANSI_CYAN}Parser {Colors.ANSI_BOLD_WHITE}returned {Colors.ANSI_LIGHT_RED}None")
        else:
            return print(f"{testcase} (❌): Parser returned None")

    e = Evaluator(parser_result, tz="Europe/Berlin")
    evaluator_result = e.evaluate()

    if evaluator_result is None:
        if not disable_colored_output:
            return print(f"{Colors.ANSI_RED}{testcase} (❌): {Colors.ANSI_CYAN}Evaluator {Colors.ANSI_BOLD_WHITE}returned {Colors.ANSI_LIGHT_RED}None")
        else:
            return print(f"{testcase} (❌): Evaluator returned None")

    if not disable_colored_output:
        print(f"{Colors.ANSI_GREEN}{testcase} (✅): {Colors.ANSI_BOLD_WHITE}{evaluator_result}{Colors.ANSI_RESET}")
    else:
        print(f"{testcase} (✅): {evaluator_result}")


def main(sort=False, disable_colored_output=False, disable_no_validation=False, disable_indent=False):
    testcase_results = {}
    max_indentation = 0

    for testcase in testcases_to_run:
        if (expected_value := testcases.get(testcase)) is None:
            print(f"Invalid testcase {testcase}")     # fixme: raise Exception
        max_indentation = max(max_indentation, len(testcase))

        p = Parser(testcase)

        try:
            parser_result = p.parse()
        except BaseException as e:
            if not disable_colored_output:
                testcase_results[testcase] = StatusType.PARSER_EXCEPTION, f"{Colors.ANSI_CYAN}Parser {Colors.ANSI_BOLD_WHITE}raised an {Colors.ANSI_LIGHT_RED}exception: {Colors.ANSI_WHITE}{e}", None
            else:
                testcase_results[testcase] = StatusType.PARSER_EXCEPTION, f"Parser raised an exception: {e}", None

            continue

        if parser_result is None:
            if not disable_colored_output:
                testcase_results[testcase] = StatusType.PARSER_ERROR, f"{Colors.ANSI_CYAN}Parser {Colors.ANSI_BOLD_WHITE}returned {Colors.ANSI_LIGHT_RED}None", None
            else:
                testcase_results[testcase] = StatusType.PARSER_ERROR, "Parser returned None", None

            continue

        e = Evaluator(parser_result, tz="Europe/Berlin")

        try:
            evaluator_result = e.evaluate()
        except BaseException as e:
            if not disable_colored_output:
                testcase_results[testcase] = StatusType.EVALUATOR_EXCEPTION, f"{Colors.ANSI_CYAN}Evaluator {Colors.ANSI_BOLD_WHITE}raised an {Colors.ANSI_LIGHT_RED}exception: {Colors.ANSI_WHITE}{e}", None
            else:
                testcase_results[testcase] = StatusType.EVALUATOR_EXCEPTION, f"Evaluator raised an exception: {e}", None

            continue

        if evaluator_result is None:
            if not disable_colored_output:
                testcase_results[testcase] = StatusType.EVALUATOR_ERROR, f"{Colors.ANSI_CYAN}Evaluator {Colors.ANSI_BOLD_WHITE}returned {Colors.ANSI_LIGHT_RED}None", None
            else:
                testcase_results[testcase] = StatusType.EVALUATOR_ERROR, "Evaluator returned None", None

            continue

        if expected_value is None:
            if not disable_no_validation:
                testcase_results[testcase] = StatusType.NO_VALIDATION, evaluator_result, None
            continue

        if evaluator_result != expected_value:
            testcase_results[testcase] = StatusType.WRONG_RESULT, f"Expected: '{expected_value}', got: '{evaluator_result}'", None
            continue

        testcase_results[testcase] = StatusType.SUCCESS, "", evaluator_result

    testcase_results_keys = list(testcase_results.keys())

    if sort:
        testcase_results_keys.sort(key=lambda v: testcase_results[v][0])

    overall_results = {
        StatusType.SUCCESS: 0,
        StatusType.PARSER_ERROR: 0,
        StatusType.PARSER_EXCEPTION: 0,
        StatusType.EVALUATOR_ERROR: 0,
        StatusType.EVALUATOR_EXCEPTION: 0,
        StatusType.WRONG_RESULT: 0,
        StatusType.NO_VALIDATION: 0
    }

    for testcase in testcase_results_keys:
        status_type, message, result = testcase_results[testcase]
        spaces = " " * (max_indentation - len(testcase) + 2) if not disable_indent else " "

        overall_results[status_type] += 1

        if not disable_colored_output:
            if status_type == StatusType.SUCCESS:
                print(f"{Colors.ANSI_GREEN}{testcase} (✅):{spaces}{Colors.ANSI_WHITE}{result}{Colors.ANSI_RESET}")
            elif status_type == StatusType.NO_VALIDATION:
                print(f"{Colors.ANSI_YELLOW}{testcase} (⚠️):{spaces}{Colors.ANSI_WHITE}{message}{Colors.ANSI_RESET}")
            else:
                print(f"{Colors.ANSI_RED}{testcase} (❌):{spaces}{Colors.ANSI_BOLD_WHITE}{message}{Colors.ANSI_RESET}")
        else:
            if status_type == StatusType.SUCCESS:
                print(f"{testcase} (✅):{spaces}{result}")
            elif status_type == StatusType.NO_VALIDATION:
                print(f"{testcase} (⚠️):{spaces}{message}")
            else:
                print(f"{testcase} (❌):{spaces}{message}")

    if not disable_colored_output:
        print("\n")
        print(f"{Colors.ANSI_GREEN}Successfully tests:         {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.SUCCESS]}/{len(testcase_results)}")
        print(f"{Colors.ANSI_YELLOW}No validation tests:        {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.NO_VALIDATION]}/{len(testcase_results)}")
        print(f"{Colors.ANSI_RED}Wrong result tests:         {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.WRONG_RESULT]}/{len(testcase_results)}")
        print()
        print(f"{Colors.ANSI_RED}Parser returned None:       {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.PARSER_EXCEPTION]}/{len(testcase_results)}")
        print(f"{Colors.ANSI_LIGHT_RED}{Colors.ANSI_UNDERLINE}Parser exceptions:          {Colors.ANSI_RESET}{Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.PARSER_ERROR]}/{len(testcase_results)}")
        print(f"{Colors.ANSI_RED}Evaluator returned None:    {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.EVALUATOR_ERROR]}/{len(testcase_results)}")
        print(f"{Colors.ANSI_LIGHT_RED}{Colors.ANSI_UNDERLINE}Evaluator exceptions:       {Colors.ANSI_RESET}{Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.EVALUATOR_EXCEPTION]}/{len(testcase_results)}")
    else:
        print("\n")
        print(f"Successful tests:           {overall_results[StatusType.SUCCESS]}/{len(testcase_results)}")
        print(f"No validation tests:        {overall_results[StatusType.NO_VALIDATION]}/{len(testcase_results)}")
        print(f"Wrong result tests:         {overall_results[StatusType.WRONG_RESULT]}/{len(testcase_results)}")
        print(f"Parser returned None:       {overall_results[StatusType.PARSER_ERROR]}/{len(testcase_results)}")
        print(f"Parser exceptions:          {overall_results[StatusType.PARSER_EXCEPTION]}/{len(testcase_results)}")
        print(f"Evaluator returned None:    {overall_results[StatusType.EVALUATOR_ERROR]}/{len(testcase_results)}")
        print(f"Evaluator exceptions:       {overall_results[StatusType.EVALUATOR_EXCEPTION]}/{len(testcase_results)}")

    exit(int(overall_results[StatusType.SUCCESS] != len(testcase_results)))


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description="Runs the testcases.")
    argument_parser.add_argument("-t", "--test", help="Runs a specific testcase.", type=str)
    argument_parser.add_argument("-s", "--sort", help="Sorts the testcases by their status.", action="store_true")
    argument_parser.add_argument("-nc", "--no-colors", help="Disables colored output.", action="store_true")
    argument_parser.add_argument("-nn", "--disable-no-validation", help="Disables the no validation testcase.", action="store_true")
    argument_parser.add_argument("-ni", "--disable-indent", help="Disables the overall indentation.", action="store_true")
    args = argument_parser.parse_args()

    if args.test is None:
        main(sort=args.sort, disable_colored_output=args.no_colors, disable_no_validation=args.disable_no_validation, disable_indent=args.disable_indent)
    else:
        run_testcase(args.test, disable_colored_output=args.no_colors)
