from timezonefinder import TimezoneFinder
from typing import Tuple


class TimeZoneManager(TimezoneFinder):

    def __init__(self):
        super(TimeZoneManager, self).__init__(in_memory=True)

    def get_coordinates(self, timezone: str) -> Tuple[float, float]:
        coords = self.get_geometry(tz_name=timezone, coords_as_pairs=True)

        while not isinstance(coords[0], Tuple):
            coords = coords[len(coords) // 2]

        coords: Tuple[float, float] = coords[len(coords) // 2]

        # timezone = self.timezone_at(lng=coords[0] + 1, lat=coords[1])
        # TODO: needs to be improved, at the moment it's just a small fix, not tested if it works with all timezones
        # TODO: add testcases for ALL timezones if possible to check if the "+1" fix is working
        # at the moment it returns "Europe/Belgium" if the timezone "Europe/Berlin" is used -> the "+1" on longitude fixes that

        return coords[0] + 1, coords[1]
