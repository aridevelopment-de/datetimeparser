from datetime import datetime, timedelta

from .baseclasses import *

class Evaluator:
    def __init__(self, parsed_object: list):
        self.parsed_object = parsed_object
    
    def evaluate(self) -> datetime:
        out = ""
        if len(self.parsed_object) == 2:
            for object_type in self.parsed_object:
                if isinstance(object_type, AbsoluteDateTime):
                    out += f"{object_type.year}-{object_type.month}-{object_type.day} "
                    
                if isinstance(object_type, AbsoluteClockTime):
                    out += f"{object_type.hour}:{object_type.minute}:{object_type.second}"
        else:
            if isinstance(self.parsed_object[0], AbsoluteDateTime):
                out += f"{self.parsed_object[0].year}-{self.parsed_object[0].month}-{self.parsed_object[0].day} 0:00:00"
            if isinstance(self.parsed_object[0], AbsoluteClockTime):
                out += f"{datetime.strftime(datetime.today(), '%Y-%m-%d')} {self.parsed_object[0].hour}:{self.parsed_object[0].minute}:{self.parsed_object[0].second}"
        if out:
            try:
                dt_object = datetime.strptime(out, "%Y-%m-%d %H:%M:%S")
                return dt_object
            except ValueError:
                return None
