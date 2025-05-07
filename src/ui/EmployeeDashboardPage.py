from tkinter import ttk


class EmployeeDashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Employee Dashboard", font=("Helvetica", 16)).pack(pady=20)

        ttk.Button(
            self,
            text="Update Availability",
            command=lambda: controller.show_frame("UpdateAvailabilityPage"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="View Schedule",
            command=lambda: controller.show_frame("ViewSchedulePage"),
        ).pack(pady=10)
