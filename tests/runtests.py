import importlib
import time

TESTS = [
    'absolute_datetimeformats',
    'absolute_prepositions',
    'relative_events'
    # 'relative_datetimes'
]

for test in TESTS:
    print("=" * 6, f"TEST: {test}", end=" " + ("=" * 6) + "\n")
    print()

    importlib.import_module(test, package=".")

    print()

    time.sleep(.1)