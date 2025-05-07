import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from ui.LoginPage import LoginPage
from ui.EmployeePage import EmployeePage
from ui.ManagerPage import ManagerPage
from ui.SettingsPage import SettingsPage
from ui.CreateSchedulePage import CreateSchedulePage
from ui.EmployeeDashboardPage import EmployeeDashboardPage


class App(ThemedTk):
    def __init__(self):
        super().__init__(theme="equilux")
        self.title("Scheduling App")
        self.geometry("600x600")
        style = ttk.Style(self)
        style.configure("TLabel", foreground="white", background="#333333")
        style.configure("TFrame", background="#333333")
        style.configure("TButton", background="#444444", foreground="white")
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        self.user = None
        self.chosen_schedule = None
        for temp_page in (
            LoginPage,
            EmployeePage,
            ManagerPage,
            CreateSchedulePage,
            SettingsPage,
            EmployeeDashboardPage,
        ):
            page_name = temp_page.__name__
            frame = temp_page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
