from tkinter import ttk


class ManagerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Top-center label
        title_label = ttk.Label(self, text="Manager Dashboard", font=("Helvetica", 16))
        title_label.pack(pady=20)

        ttk.Button(
            self,
            text="Create Schedules",
            command=lambda: controller.show_frame("CreateSchedulePage"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Change Your Availability",
            command=lambda: controller.show_frame("EmployeePage"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Company Settings",
            command=lambda: controller.show_frame("SettingsPage"),
        ).pack(pady=10)

        ttk.Button(
            self, text="Sign Out", command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=10)
