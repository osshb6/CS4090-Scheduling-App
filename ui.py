#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scheduling App")
        self.geometry("400x300")
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}

        for temp_page in (LoginPage, CreateAccountPage):
            page_name = temp_page.__name__
            frame = temp_page(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Username").pack(pady=10)
        self.username = ttk.Entry(self)
        self.username.pack(pady=5)

        ttk.Button(self, text="Login", command=lambda: print(self.username.get())).pack(pady=10)

        ttk.Label(self, text="Click here to make account").pack(pady=10)
        ttk.Button(self, text="Create Account", command=lambda: controller.show_frame("CreateAccountPage")).pack()


class CreateAccountPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Create Your Account").pack(pady=10)
        self.new_user = ttk.Entry(self)
        self.new_user.pack(pady=5)

        ttk.Button(self, text="Register", command=lambda: print(f"Registered: {self.new_user.get()}")).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginPage")).pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
