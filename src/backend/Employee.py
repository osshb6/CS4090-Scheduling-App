class Employee:
    def __init__(self, id: int, name: str, position: str, title: str) -> None:
        self.id: int = id
        self.name: str = name
        self.position: str = position
        self.title: str = title
        #key is day of the week and availability is boolean. Default is available every day of the week
        self.availability: dict = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}
