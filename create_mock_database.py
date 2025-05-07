from src.backend.Database import (
    AvailabilityTable,
    DatabaseConnection,
    ShiftTable,
    UserTable,
)


DatabaseConnection(db_path="database/mock_company.db")
UserTable().create_user("Alice", "General Manager", "Manager")
UserTable().create_user("Bob", "Assistant Manager", "Manager")
UserTable().create_user("Clara", "Cook")
UserTable().create_user("Dan", "Cook")
UserTable().create_user("Eva", "Cook")
UserTable().create_user("Frank", "Cashier")
UserTable().create_user("Grace", "Cashier")
UserTable().create_user("Henry", "Cashier")

# Alice
AvailabilityTable().add_availability(1, "Monday", "14:00", "22:00")
AvailabilityTable().add_availability(1, "Wednesday", "14:00", "22:00")
AvailabilityTable().add_availability(1, "Thursday", "14:00", "22:00")
AvailabilityTable().add_availability(1, "Sunday", "06:00", "14:00")

# Bob
AvailabilityTable().add_availability(2, "Monday", "06:00", "14:00")
AvailabilityTable().add_availability(2, "Tuesday", "06:00", "14:00")
AvailabilityTable().add_availability(2, "Friday", "14:00", "22:00")
AvailabilityTable().add_availability(2, "Saturday", "14:00", "22:00")

# Clara
AvailabilityTable().add_availability(3, "Monday", "06:00", "14:00")
AvailabilityTable().add_availability(3, "Wednesday", "14:00", "22:00")
AvailabilityTable().add_availability(3, "Thursday", "06:00", "14:00")
AvailabilityTable().add_availability(3, "Friday", "06:00", "14:00")
AvailabilityTable().add_availability(3, "Saturday", "06:00", "14:00")
AvailabilityTable().add_availability(3, "Sunday", "14:00", "22:00")

# Dan
AvailabilityTable().add_availability(4, "Tuesday", "06:00", "14:00")
AvailabilityTable().add_availability(4, "Wednesday", "06:00", "14:00")
AvailabilityTable().add_availability(4, "Thursday", "14:00", "22:00")
AvailabilityTable().add_availability(4, "Friday", "14:00", "22:00")

# Eva
AvailabilityTable().add_availability(5, "Monday", "06:00", "14:00")
AvailabilityTable().add_availability(5, "Tuesday", "14:00", "22:00")
AvailabilityTable().add_availability(5, "Thursday", "06:00", "14:00")
AvailabilityTable().add_availability(5, "Saturday", "06:00", "14:00")
AvailabilityTable().add_availability(5, "Sunday", "06:00", "14:00")

# Frank
AvailabilityTable().add_availability(6, "Monday", "14:00", "22:00")
AvailabilityTable().add_availability(6, "Wednesday", "14:00", "22:00")
AvailabilityTable().add_availability(6, "Thursday", "06:00", "14:00")
AvailabilityTable().add_availability(6, "Friday", "06:00", "14:00")
AvailabilityTable().add_availability(6, "Saturday", "14:00", "22:00")

# Grace
AvailabilityTable().add_availability(7, "Tuesday", "06:00", "14:00")
AvailabilityTable().add_availability(7, "Wednesday", "06:00", "14:00")
AvailabilityTable().add_availability(7, "Thursday", "14:00", "22:00")
AvailabilityTable().add_availability(7, "Sunday", "14:00", "22:00")

# Henry
AvailabilityTable().add_availability(8, "Monday", "06:00", "14:00")
AvailabilityTable().add_availability(8, "Tuesday", "06:00", "14:00")
AvailabilityTable().add_availability(8, "Friday", "14:00", "22:00")
AvailabilityTable().add_availability(8, "Saturday", "06:00", "14:00")
AvailabilityTable().add_availability(8, "Sunday", "14:00", "22:00")

# Morning
ShiftTable().create_shift(None, "Monday", "06:00", "14:00")
ShiftTable().create_shift(None, "Monday", "06:00", "14:00")
ShiftTable().create_shift(None, "Tuesday", "06:00", "14:00")
ShiftTable().create_shift(None, "Tuesday", "06:00", "14:00")
ShiftTable().create_shift(None, "Wednesday", "06:00", "14:00")
ShiftTable().create_shift(None, "Wednesday", "06:00", "14:00")
ShiftTable().create_shift(None, "Thursday", "06:00", "14:00")
ShiftTable().create_shift(None, "Thursday", "06:00", "14:00")
ShiftTable().create_shift(None, "Friday", "06:00", "14:00")
ShiftTable().create_shift(None, "Friday", "06:00", "14:00")
ShiftTable().create_shift(None, "Saturday", "06:00", "14:00")
ShiftTable().create_shift(None, "Saturday", "06:00", "14:00")
ShiftTable().create_shift(None, "Sunday", "06:00", "14:00")
ShiftTable().create_shift(None, "Sunday", "06:00", "14:00")

# Evening
ShiftTable().create_shift(None, "Monday", "14:00", "22:00")
ShiftTable().create_shift(None, "Monday", "14:00", "22:00")
ShiftTable().create_shift(None, "Monday", "14:00", "22:00")
ShiftTable().create_shift(None, "Tuesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Tuesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Tuesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Wednesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Wednesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Wednesday", "14:00", "22:00")
ShiftTable().create_shift(None, "Thursday", "14:00", "22:00")
ShiftTable().create_shift(None, "Thursday", "14:00", "22:00")
ShiftTable().create_shift(None, "Thursday", "14:00", "22:00")
ShiftTable().create_shift(None, "Friday", "14:00", "22:00")
ShiftTable().create_shift(None, "Friday", "14:00", "22:00")
ShiftTable().create_shift(None, "Friday", "14:00", "22:00")
ShiftTable().create_shift(None, "Saturday", "14:00", "22:00")
ShiftTable().create_shift(None, "Saturday", "14:00", "22:00")
ShiftTable().create_shift(None, "Saturday", "14:00", "22:00")
ShiftTable().create_shift(None, "Sunday", "14:00", "22:00")
ShiftTable().create_shift(None, "Sunday", "14:00", "22:00")
ShiftTable().create_shift(None, "Sunday", "14:00", "22:00")
