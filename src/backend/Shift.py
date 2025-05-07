class Shift:
    def __init__(self, id: int, user_id: int, day_of_week: str, start_time: str, end_time: str, employee=None) -> None:
        self.id: int = id
        self.user_id = user_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.employee = employee

