from datetime import datetime


class Result:
    time: datetime
    timezone: str
    coordinates: tuple[float, float]

    def __init__(self, time, timezone: str, coordinates: tuple[float, float] = None):
        self.time = time
        self.timezone = timezone
        self.coordinates = coordinates

    def __repr__(self):
        out: str = "'None'"
        if self.coordinates:
            out: str = f"[longitude='{self.coordinates[0]}', latitude='{self.coordinates[1]}]'"
        return f"<Result: time='{self.time}', timezone='{self.timezone}', coordinates={out}>"
