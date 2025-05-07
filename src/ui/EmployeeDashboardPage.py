from tkinter import ttk

class EmployeeDashboardPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Style definitions
        style = ttk.Style()
        style.configure("Dashboard.TLabel", font=("Segoe UI", 12), foreground="white", background="#333333")
        style.configure("Dashboard.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Centering content
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        ttk.Label(
            center_frame,
            text="Employee Dashboard",
            style="Dashboard.TLabel",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 20))

        # Button: Update Availability
        ttk.Button(
            center_frame,
            text="Update Availability",
            style="Dashboard.TButton",
            command=lambda: controller.show_frame("UpdateAvailabilityPage")
        ).pack(pady=10, padx=100)

        # Button: View Schedule
        ttk.Button(
            center_frame,
            text="View Schedule",
            style="Dashboard.TButton",
            command=lambda: controller.show_frame("ViewSchedulePage")
        ).pack(pady=10, padx=100)

        # Button: Sign Out
        ttk.Button(
            center_frame,
            text="Sign Out",
            style="Dashboard.TButton",
            command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=20, padx=100)
