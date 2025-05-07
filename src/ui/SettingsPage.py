from tkinter import ttk

class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Apply custom styles
        style = ttk.Style()
        style.configure("Settings.TLabel", font=("Segoe UI", 12), foreground="white", background="#333333")
        style.configure("Settings.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Centered layout container
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        ttk.Label(center_frame, text="Company Settings", style="Settings.TLabel",
                  font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        # Settings action buttons
        actions = [
            ("Get Employees", lambda: print("call db functions and print somewhere")),
            ("Delete Employee", lambda: print("call db functions and print somewhere")),
            ("Promote Employee", lambda: print("call db functions and print somewhere")),
            ("Sign Out", lambda: controller.show_frame("LoginPage")),
            ("Back", lambda: controller.show_frame("ManagerPage")),
        ]

        for text, cmd in actions:
            ttk.Button(center_frame, text=text, style="Settings.TButton", command=cmd).pack(pady=10, padx=100)
