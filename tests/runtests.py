import argparse
import datetime

from typing import Optional, Tuple, Union

try:
    from testcases import ThrowException, ReturnNone, testcases
    from colors import Colors

    from datetimeparser.parser import Parser
    from datetimeparser.evaluator import Evaluator
except (ImportError, ModuleNotFoundError):
    import sys

    sys.path.insert(0, "..")

    from testcases import ThrowException, ReturnNone, testcases
    from colors import Colors

    from datetimeparser.parser import Parser
    from datetimeparser.evaluator import Evaluator


class StatusType:
    SUCCESS = 0
    NO_VALIDATION = 1
    PARSER_RETURNS_NONE = 2
    PARSER_EXCEPTION = 3
    EVALUATOR_RETURNS_NONE = 4
    EVALUATOR_EXCEPTION = 5
    WRONG_RESULT = 6


def get_testcase_results(
        testcase: str, expected_value: datetime.datetime = None
) -> Tuple[int, Optional[Union[str, datetime.datetime]]]:
    parser = Parser(testcase)

    try:
        parser_result = parser.parse()
    except BaseException as error:
        if expected_value == ThrowException:
            return StatusType.SUCCESS, "Parser threw exception but it was expected"

        return StatusType.PARSER_EXCEPTION, str(error)

    if parser_result is None:
        return StatusType.PARSER_RETURNS_NONE, None

    evaluator = Evaluator(parser_result, tz="Europe/Berlin")

    try:
        evaluator_result = evaluator.evaluate()
    except BaseException as error:
        if expected_value == ThrowException:
            return StatusType.SUCCESS, "Evaluator threw exception but it was expected"

        return StatusType.EVALUATOR_EXCEPTION, str(error)

    if evaluator_result is None:
        return StatusType.EVALUATOR_RETURNS_NONE, None

    if expected_value is None:
        return StatusType.NO_VALIDATION, evaluator_result

    if evaluator_result != expected_value:
        return StatusType.WRONG_RESULT, evaluator_result

    return StatusType.SUCCESS, evaluator_result


def evaluate_testcases(testcase_results: dict, disable_color=False, disable_indent=False):
    """
    Evaluates the testcases

    :param testcase_results: {category: [{testcase: None, status: None, result: None, info: None, expected_value: None}]}
    :param disable_color: If the color should be disabled
    :param disable_indent: If the indent should be disabled
    :return: None
    """
    overall_results = {
        StatusType.SUCCESS: 0,
        StatusType.PARSER_RETURNS_NONE: 0,
        StatusType.PARSER_EXCEPTION: 0,
        StatusType.EVALUATOR_RETURNS_NONE: 0,
        StatusType.EVALUATOR_EXCEPTION: 0,
        StatusType.WRONG_RESULT: 0,
        StatusType.NO_VALIDATION: 0
    }

    len_testcases = 0

    for category in testcase_results:
        if not disable_color:
            print(f"\n{Colors.ANSI_BOLD_WHITE}{category}")
        else:
            print(f"\n{category}")

        max_indentation = 0

        for test_case_data in testcase_results[category]:
            max_indentation = max(max_indentation, len(test_case_data["testcase"]))
            len_testcases += 1

        for test_case_data in sorted(testcase_results[category], key=lambda x: x["status"], reverse=True):
            test_case = test_case_data["testcase"]
            status = test_case_data["status"]
            result = test_case_data["result"]
            info = test_case_data["info"]
            expected_value = test_case_data["expected_value"]
            spaces = " " * (max_indentation - len(test_case) + 4) if not disable_indent else " "

            if not disable_color:
                if status == StatusType.SUCCESS:
                    print(f"\t└ {Colors.ANSI_GREEN}{test_case}{spaces}{Colors.ANSI_WHITE}{result}{Colors.ANSI_RESET}")
                elif status == StatusType.NO_VALIDATION:
                    print(f"\t└ {Colors.ANSI_YELLOW}{test_case}{spaces}{Colors.ANSI_WHITE}{result}{Colors.ANSI_RESET}")
                elif StatusType.NO_VALIDATION < status < StatusType.WRONG_RESULT:
                    if status in (StatusType.PARSER_RETURNS_NONE, StatusType.EVALUATOR_RETURNS_NONE):
                        message = f"{Colors.ANSI_CYAN}{'Parser' if status == StatusType.PARSER_RETURNS_NONE else 'Evaluator'} {Colors.ANSI_BOLD_WHITE}returned {Colors.ANSI_LIGHT_RED}None"
                    elif status in (StatusType.PARSER_EXCEPTION, StatusType.EVALUATOR_RETURNS_NONE):
                        message = f"{Colors.ANSI_CYAN}{'Parser' if status == StatusType.PARSER_EXCEPTION else 'Evaluator'} {Colors.ANSI_BOLD_WHITE}raised an {Colors.ANSI_LIGHT_RED}exception: {Colors.ANSI_WHITE}{info}"
                    else:
                        continue

                    print(f"\t└ {Colors.ANSI_RED}{test_case}{spaces}{Colors.ANSI_RESET}{message}{Colors.ANSI_RESET}")
                elif status == StatusType.WRONG_RESULT:
                    print(f"\t└ {Colors.ANSI_RED}{test_case}{spaces}{Colors.ANSI_BOLD_WHITE}Expected: '{expected_value}', got: '{result}'{Colors.ANSI_RESET}")
            else:
                if status == StatusType.SUCCESS:
                    print(f"\t└ {test_case}{spaces}{result}")
                elif status == StatusType.NO_VALIDATION:
                    print(f"\t└ {test_case}{spaces}{result}")
                elif StatusType.NO_VALIDATION < status < StatusType.WRONG_RESULT:
                    if status in (StatusType.PARSER_RETURNS_NONE, StatusType.EVALUATOR_RETURNS_NONE):
                        message = f"{'Parser' if status == StatusType.PARSER_RETURNS_NONE else 'Evaluator'} returned None"
                    elif status in (StatusType.PARSER_EXCEPTION, StatusType.EVALUATOR_RETURNS_NONE):
                        message = f"{'Parser' if status == StatusType.PARSER_EXCEPTION else 'Evaluator'} raised an exception: {info}"
                    else:
                        continue

                    print(f"\t└ {test_case}{spaces}{message}")
                elif status == StatusType.WRONG_RESULT:
                    print(f"\t└ {test_case}{spaces}Expected: '{expected_value}', got: '{result}'")

            overall_results[status] += 1

    if not disable_color:
        print("\n")
        print(f"{Colors.ANSI_GREEN}Successfully tests:         {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.SUCCESS]}/{len_testcases}")
        print(f"{Colors.ANSI_YELLOW}No validation tests:        {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.NO_VALIDATION]}/{len_testcases}")
        print(f"{Colors.ANSI_RED}Wrong result tests:         {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.WRONG_RESULT]}/{len_testcases}")
        print()
        print(f"{Colors.ANSI_RED}Parser returned None:       {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.PARSER_EXCEPTION]}/{len_testcases}")
        print(f"{Colors.ANSI_LIGHT_RED}{Colors.ANSI_UNDERLINE}Parser exceptions:          {Colors.ANSI_RESET}{Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.PARSER_RETURNS_NONE]}/{len_testcases}")
        print(f"{Colors.ANSI_RED}Evaluator returned None:    {Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.EVALUATOR_RETURNS_NONE]}/{len_testcases}")
        print(f"{Colors.ANSI_LIGHT_RED}{Colors.ANSI_UNDERLINE}Evaluator exceptions:       {Colors.ANSI_RESET}{Colors.ANSI_BOLD_WHITE}{overall_results[StatusType.EVALUATOR_EXCEPTION]}/{len_testcases}")
    else:
        print("\n")
        print(f"Successful tests:           {overall_results[StatusType.SUCCESS]}/{len_testcases}")
        print(f"No validation tests:        {overall_results[StatusType.NO_VALIDATION]}/{len_testcases}")
        print(f"Wrong result tests:         {overall_results[StatusType.WRONG_RESULT]}/{len_testcases}")
        print()
        print(f"Parser returned None:       {overall_results[StatusType.PARSER_RETURNS_NONE]}/{len_testcases}")
        print(f"Parser exceptions:          {overall_results[StatusType.PARSER_EXCEPTION]}/{len_testcases}")
        print(f"Evaluator returned None:    {overall_results[StatusType.EVALUATOR_RETURNS_NONE]}/{len_testcases}")
        print(f"Evaluator exceptions:       {overall_results[StatusType.EVALUATOR_EXCEPTION]}/{len_testcases}")

    exit(int(overall_results[StatusType.SUCCESS] != len_testcases))


def main(specified_category: str = None):
    data = {}  # {category: [{testcase: None, status: None, result: None, info: None, expected_value: None}]}

    for category in testcases:
        if specified_category is not None:
            if specified_category != category:
                continue

        data[category] = []

        for testcase in testcases[category]:
            status, result = get_testcase_results(testcase, testcases[category][testcase])

            data[category].append({
                "testcase": testcase,
                "status": status,
                "result": result,
                "info": result,
                "expected_value": testcases[category][testcase]
            })

    return data


if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser(description="Runs the testcases.")
    argument_parser.add_argument("-t", "--test", help="Runs a specific testcase.", type=str)
    argument_parser.add_argument("-c", "--category", help="Runs a specific category of testcases.", type=str)
    argument_parser.add_argument("-nc", "--no-colors", help="Disables colored output.", action="store_true")
    argument_parser.add_argument("-ni", "--no-indent", help="Disables the overall indentation.", action="store_true")
    args = argument_parser.parse_args()

    if args.test is None:
        result = main(specified_category=args.category)
        evaluate_testcases(result, disable_color=args.no_colors, disable_indent=args.no_indent)
    else:
        status, result = get_testcase_results(args.test, None)

        resulting_data = {
            "User-Specified": [{
                "testcase": args.test,
                "status": status,
                "result": result,
                "info": result,
                "expected_value": None
            }]
        }

        evaluate_testcases(resulting_data, disable_color=args.no_colors, disable_indent=args.no_indent)
