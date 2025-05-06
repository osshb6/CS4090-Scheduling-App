import sqlite3
import sys
import os


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls, db_path="database/data.db", schema_path="database/schema.sql"):
        print("path" + sys.path[0])
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # If DB doesn't exist, create it and apply schema
            db_exists = os.path.exists(db_path)
            cls._connection = sqlite3.connect(db_path)
            if not db_exists:
                print("trying to initialize new DB")
                with open(schema_path, "r") as f:
                    cls._connection.executescript(f.read())

        return cls._instance

    def get_connection(self):
        return self._connection

    def close_connection(self):
        if self._connection:
            self._connection.close()
            self._connection = None
            DatabaseConnection._instance = None


class UserTable:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def create_user(self, name, title, role="Employee"):
        self.cursor.execute(
            "INSERT INTO Users (Name, Title, Role) VALUES (?, ?, ?)",
            (name, title, role),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_user(self, name):
        self.cursor.execute("SELECT * FROM Users WHERE Name = ?", (name,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM Users")
        return self.cursor.fetchall()

    def update_user(self, user_id, name=None, title=None, role=None):
        if name:
            self.cursor.execute(
                "UPDATE Users SET Name = ? WHERE id = ?", (name, user_id)
            )
        if title:
            self.cursor.execute(
                "UPDATE Users SET Title = ? WHERE id = ?", (title, user_id)
            )
        if role:
            self.cursor.execute(
                "UPDATE Users SET Role = ? WHERE id = ?", (role, user_id)
            )
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
        self.conn.commit()


class AvailabilityTable:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def add_availability(self, user_id, day_of_week, start_time, end_time):
        self.cursor.execute(
            """
            INSERT INTO Availability (user_id, day_of_week, start_time, end_time)
            VALUES (?, ?, ?, ?)""",
            (user_id, day_of_week, start_time, end_time),
        )
        self.conn.commit()

    def get_availability_by_user(self, user_id):
        self.cursor.execute("SELECT * FROM Availability WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_all_availability(self):
        self.cursor.execute("SELECT * FROM Availability")
        return self.cursor.fetchall()

    def delete_availability(self, availability_id):
        self.cursor.execute("DELETE FROM Availability WHERE id = ?", (availability_id,))
        self.conn.commit()


class ShiftTable:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def create_shift(self, user_id, day_of_week, start_time, end_time):
        self.cursor.execute(
            """
            INSERT INTO Shifts (user_id, day_of_week, start_time, end_time)
            VALUES (?, ?, ?, ?)""",
            (user_id, day_of_week, start_time, end_time),
        )
        self.conn.commit()

    def get_shifts_by_user(self, user_id):
        self.cursor.execute("SELECT * FROM Shifts WHERE user_id = ?", (user_id,))
        return self.cursor.fetchall()

    def get_all_shifts(self):
        self.cursor.execute("SELECT * FROM Shifts")
        return self.cursor.fetchall()

    def update_shift(self, shift_id, start_time=None, end_time=None):
        if start_time:
            self.cursor.execute(
                "UPDATE Shifts SET start_time = ? WHERE id = ?", (start_time, shift_id)
            )
        if end_time:
            self.cursor.execute(
                "UPDATE Shifts SET end_time = ? WHERE id = ?", (end_time, shift_id)
            )
        self.conn.commit()

    def delete_shift(self, name):
        self.cursor.execute("DELETE FROM Shifts WHERE name = ?", (name,))
        self.conn.commit()


class OptimizationLogTable:
    def __init__(self):
        self.conn = DatabaseConnection().get_connection()
        self.cursor = self.conn.cursor()

    def log_optimization(self, run_date, criteria_used, success_rate):
        self.cursor.execute(
            """
            INSERT INTO OptimizationLogs (run_date, criteria_used, success_rate)
            VALUES (?, ?, ?)""",
            (run_date, criteria_used, success_rate),
        )
        self.conn.commit()

    def get_all_logs(self):
        self.cursor.execute("SELECT * FROM OptimizationLogs")
        return self.cursor.fetchall()

    def delete_log(self, log_id):
        self.cursor.execute("DELETE FROM OptimizationLogs WHERE id = ?", (log_id,))
        self.conn.commit()
