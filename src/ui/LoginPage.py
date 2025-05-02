from tkinter import ttk


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ttk.Label(self, text="Username").pack(pady=10)
        self.username = ttk.Entry(self)
        self.username.pack(pady=5)

        ttk.Button(self, text="Login", command=lambda: print(self.username.get())).pack(
            pady=10
        )

        ttk.Label(self, text="Click here to make account").pack(pady=10)
        ttk.Button(
            self,
            text="Create Account",
            command=lambda: controller.show_frame("CreateAccountPage"),
        ).pack()
