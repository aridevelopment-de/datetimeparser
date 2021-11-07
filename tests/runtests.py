import time

try:
    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes
except (ImportError, ModuleNotFoundError):
    import sys

    sys.path.insert(0, "..")

    import absolute_datetimeformats
    import absolute_prepositions
    import relative_events
    import relative_datetimes

TESTS = [
    absolute_datetimeformats,
    absolute_prepositions,
    relative_events
    # relative_datetimes
]

for test in TESTS:
    print("=" * 6, f"TEST: {test}", end=" " + ("=" * 6) + "\n")
    print()

    getattr(test, "run")()

    print()

    time.sleep(.1)