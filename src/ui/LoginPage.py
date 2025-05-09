from tkinter import ttk, messagebox
from backend.Database import UserTable
from backend.Employee import Employee


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Style customization for labels and buttons (optional)
        style = ttk.Style()
        style.configure(
            "Login.TLabel",
            font=("Segoe UI", 12),
            foreground="white",
            background="#333333",
        )
        style.configure("Login.TEntry", padding=5)
        style.configure("Login.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Wrapper frame for vertical centering
        frame = ttk.Frame(self)
        frame.pack(expand=True)

        # Title label
        ttk.Label(
            frame,
            text="Login to Scheduling App",
            style="Login.TLabel",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(100, 10))

        # Username label + entry
        ttk.Label(frame, text="Username:", style="Login.TLabel").pack(pady=5, padx=200)
        self.username = ttk.Entry(frame, style="Login.TEntry", width=30)
        self.username.pack(pady=5, padx=200)

        # Login button
        ttk.Button(
            frame,
            text="Login",
            style="Login.TButton",
            command=lambda: self.validate_login(self.username.get()),
        ).pack(pady=15, padx=200)

    def validate_login(self, user_string):
        user = UserTable().get_user(user_string)
        if user:
            self.controller.user = Employee(
                id=user[0], name=user[1], position=user[2], title=user[3]
            )
            if self.controller.user.title == "Manager":
                self.controller.show_frame("ManagerPage")
            else:
                self.controller.show_frame("EmployeeDashboardPage")
        else:
            messagebox.showerror("Login Failed", "No user found with that name.")
