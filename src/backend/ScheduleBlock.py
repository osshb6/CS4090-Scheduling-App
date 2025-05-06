from TimeFrame import TimeFrame
from typing import List
from backend.Employee import Employee


class ScheduleBlock:
    def __init__(self, frame: TimeFrame, staff: List[Employee]) -> None:
        self.frame: TimeFrame = frame
        self.staff: List[Employee] = staff
