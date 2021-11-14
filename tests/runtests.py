import time

try:
    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes
    import general_tests
    from TestValidator import TestValidator
except (ImportError, ModuleNotFoundError):
    import sys

    sys.path.insert(0, "..")

    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes
    import general_tests
    from TestValidator import TestValidator

TESTS = [
    absolute_datetimeformats,
    absolute_prepositions,
    relative_events,
    relative_datetimes,
    general_tests
]

for test in TESTS:
    print("\u001B[0;1m" + "=" * 6, f"TEST: {test}", end=" " + ("=" * 6) + "\u001b[0m\n")
    print()

    time.sleep(.1)

    validator = TestValidator(getattr(test, "tests"), getattr(test, "validation"))
    validator.validate()

    print()

