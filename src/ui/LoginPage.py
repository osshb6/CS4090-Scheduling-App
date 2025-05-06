from tkinter import ttk, messagebox
from src.backend.Database import UserTable
from src.backend.Employee import Employee


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="Username").pack(pady=10)
        self.username = ttk.Entry(self)
        self.username.pack(pady=5)

        ttk.Button(self, text="Login", command=lambda: self.validate_login(self.username.get())).pack(
            pady=10
        )

    def validate_login(self, user_string):
        user = UserTable().get_user(user_string)
        if user:
            self.controller.user = Employee(id=user[0], name=user[1], position=user[2], title=user[3])
            if self.controller.user.title == "Manager":
                self.controller.show_frame("ManagerPage")
            else:
                self.controller.show_frame("EmployeePage")
        else:
            messagebox.showerror("Login Failed", "No user found with that name.")

