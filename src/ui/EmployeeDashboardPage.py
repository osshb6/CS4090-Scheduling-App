from tkinter import ttk
import tkinter as tk

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
            command=self.view_schedule
        ).pack(pady=10, padx=100)

        # Button: Sign Out
        ttk.Button(
            center_frame,
            text="Sign Out",
            style="Dashboard.TButton",
            command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=20, padx=100)

    def view_schedule(self):
        popup = tk.Toplevel(self)
        popup.title("Optimized Schedule (Minimum Open Shifts)")
        days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        columns = ("Start Time", "End Time") + days_of_week
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.title())
        for row in self.controller.chosen_schedule:
            tree.insert("", tk.END, values=row)
        
        tree.pack(padx=20, pady=10, fill="both", expand=True)

        info_frame = ttk.Frame(popup)
        info_frame.pack(pady=5, fill="x", expand=True)
