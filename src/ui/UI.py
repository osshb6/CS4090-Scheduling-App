#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from LoginPage import LoginPage
from EmployeePage import EmployeePage
from ManagerPage import ManagerPage
from CreateSchedulePage import CreateSchedulePage
from SettingsPage import SettingsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scheduling App")
        self.geometry("400x600")
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}
        self.user = None

        for temp_page in (LoginPage, EmployeePage, ManagerPage, CreateSchedulePage, SettingsPage):
            page_name = temp_page.__name__
            frame = temp_page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = App()
    app.mainloop()
