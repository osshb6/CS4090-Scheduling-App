from typing import List
from datetime import datetime
from backend.TimeFrame import TimeFrame


class Schedule:
    def __init__(self, name: str, creation_date: datetime):
        self.name: str = name
        self.creation_date: datetime = creation_date
        self.blocks: List[List[TimeFrame]] = [[] for _ in range(7)]
