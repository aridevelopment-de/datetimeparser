import importlib
import time

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