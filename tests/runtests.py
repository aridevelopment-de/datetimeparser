import time
import sys

try:
    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes
    import general_tests

    from TestValidator import TestValidator
    from Colors import Colors
except (ImportError, ModuleNotFoundError):
    import sys

    sys.path.insert(0, "..")

    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes
    import general_tests

    from TestValidator import TestValidator
    from Colors import Colors

TESTS = [
    absolute_datetimeformats,
    absolute_prepositions,
    relative_events,
    relative_datetimes,
    general_tests
]

results = {}

for test in TESTS:
    print("\u001B[0;1m" + "=" * 6, f"TEST: {test}", end=" " + ("=" * 6) + "\u001b[0m\n")
    print()

    time.sleep(.1)

    validator = TestValidator(getattr(test, "tests"), getattr(test, "validation"))
    results[str(test)] = validator.validate()

    print()

time.sleep(.1)

print(Colors.ANSI_BOLD_WHITE + ("=" * 30), "RESULTS", ("=" * 30) + Colors.ANSI_RESET)
print()

print(Colors.ANSI_PURPLE + "Total modules:", Colors.ANSI_CYAN + str(len(TESTS)) + Colors.ANSI_RESET)
print(Colors.ANSI_PURPLE + "Total tests:", Colors.ANSI_CYAN + str(sum(map(lambda e: e[1], list(results.values())))) + Colors.ANSI_RESET)
print(Colors.ANSI_PURPLE + "Total passed:", Colors.ANSI_GREEN + str(sum(map(lambda e: e[1] - len(e[0]), list(results.values())))) + Colors.ANSI_RESET)
print(Colors.ANSI_PURPLE + "Total failed:", Colors.ANSI_RED + str(sum(map(lambda e: len(e[0]), list(results.values())))) + Colors.ANSI_RESET)
print()

for module in results:
    failed, whole = results[module]

    if failed:
        print(Colors.ANSI_PURPLE + "In Module " + Colors.ANSI_YELLOW + module + Colors.ANSI_BOLD_WHITE + ":")
        print(f"\t{Colors.ANSI_BOLD_WHITE}- {Colors.ANSI_PURPLE}Test cases: {Colors.ANSI_CYAN}{whole}")
        print(f"\t{Colors.ANSI_BOLD_WHITE}- {Colors.ANSI_PURPLE}Passed: {Colors.ANSI_GREEN}{whole - len(failed)}")
        print(f"\t{Colors.ANSI_BOLD_WHITE}- {Colors.ANSI_PURPLE}Failed: {Colors.ANSI_RED}{len(failed)}")

        for test in failed:
            print(f"\t\t{Colors.ANSI_RED}- Failed testcase: {Colors.ANSI_CYAN}{test}")

        print()

if sum(map(lambda e: len(e[0]), list(results.values()))) > 0:
    sys.exit(1)
else:
    sys.exit(0)