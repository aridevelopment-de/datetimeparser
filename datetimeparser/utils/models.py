from datetime import datetime


class Result:
    """
    The returned Result by the parse function, containing the output information

    - Attributes:
        - time (datetime): The parsed time
        - timezone (str): The used timezone
        - coordinates (Optional[tuple[float, float]]): Coordinates used for parsing

    """
    time: datetime
    timezone: str
    coordinates: tuple[float, float]

    def __init__(self, time: datetime, timezone: str, coordinates: tuple[float, float] = None):
        self.time = time
        self.timezone = timezone
        self.coordinates = coordinates

    def __repr__(self):
        out: str = "'None'"
        if self.coordinates:
            out: str = f"[longitude='{self.coordinates[0]}', latitude='{self.coordinates[1]}]'"
        return f"<Result: time='{self.time}', timezone='{self.timezone}', coordinates={out}>"

    def __str__(self):
        return self.__repr__()
