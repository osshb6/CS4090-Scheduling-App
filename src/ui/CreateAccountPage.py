from tkinter import ttk


class CreateAccountPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Create Your Account").pack(pady=10)
        self.new_user = ttk.Entry(self)
        self.new_user.pack(pady=5)

        ttk.Button(
            self,
            text="Register",
            command=lambda: print(f"Registered: {self.new_user.get()}"),
        ).pack(pady=10)
        ttk.Button(
            self,
            text="Back to Login",
            command=lambda: controller.show_frame("LoginPage"),
        ).pack()
