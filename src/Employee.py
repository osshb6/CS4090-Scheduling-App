from datetime import time, date
from typing import List
from TimeFrame import TimeFrame


class Employee:
    def __init__(self, id: int, name: str, birthdate: date, position: str):
        self.id: int = id
        self.name: str = name
        self.birthdate: date = birthdate
        self.position: str = position
        self.availability: List[List[TimeFrame]] = [[] for _ in range(7)]
