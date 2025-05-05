#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from LoginPage import LoginPage
from CreateAccountPage import CreateAccountPage
from EmployeePage import EmployeePage
from ManagerPage import ManagerPage
from CreateSchedulePage import CreateSchedulePage
from SettingsPage import SettingsPage
from pathlib import Path
from src.backend.Database import (
    DatabaseConnection,
    UserTable,
    ShiftTable,
    AvailabilityTable,
    OptimizationLogTable,
)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scheduling App")
        self.geometry("400x600")

        project_root = Path(__file__).resolve().parents[2]
        db_path = project_root / "database" / "scheduler.db"
        DatabaseConnection(db_path=db_path)

        self.user_table = UserTable()
        self.shift_table = ShiftTable()
        self.avail_table = AvailabilityTable()
        self.log_table = OptimizationLogTable()
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for Page in (
            LoginPage,
            CreateAccountPage,
            EmployeePage,
            ManagerPage,
            CreateSchedulePage,
            SettingsPage,
        ):
            name = Page.__name__
            frame = Page(container, self)
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name: str):
        self.frames[page_name].tkraise()

    def destroy(self):
        from src.backend.Database import DatabaseConnection

        DatabaseConnection().close_connection()
        super().destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
