from tkinter import ttk, BooleanVar


class EmployeePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Styling
        style = ttk.Style()
        style.configure(
            "Employee.TLabel",
            font=("Segoe UI", 12),
            foreground="white",
            background="#333333",
        )
        style.configure(
            "Employee.TCheckbutton",
            font=("Segoe UI", 11),
            background="#333333",
            foreground="white",
        )
        style.configure("Employee.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Centered content frame
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ttk.Label(
            center_frame,
            text="Set Your Availability",
            style="Employee.TLabel",
            font=("Segoe UI", 16, "bold"),
        ).pack(pady=(0, 20))

        # Instruction label
        ttk.Label(
            center_frame,
            text="Days of the week you want to work:",
            style="Employee.TLabel",
        ).pack(pady=10)

        # BooleanVars for checkboxes
        self.days = {
            day: BooleanVar()
            for day in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        }

        # Checkbox group frame (for tighter layout control)
        checkbox_frame = ttk.Frame(center_frame)
        checkbox_frame.pack(pady=10)

        for day, var in self.days.items():
            ttk.Checkbutton(
                checkbox_frame, text=day, variable=var, style="Employee.TCheckbutton"
            ).pack(anchor="w", padx=20)

        # Submit button
        ttk.Button(
            center_frame,
            text="Submit",
            style="Employee.TButton",
            command=self.submit_availability,
        ).pack(pady=(20, 10), padx=100)

        # Sign out button
        ttk.Button(
            center_frame,
            text="Sign Out",
            style="Employee.TButton",
            command=lambda: controller.show_frame("LoginPage"),
        ).pack(pady=10, padx=100)

    # debug
    def submit_availability(self):
        selected_days = [day for day, var in self.days.items() if var.get()]
        print("Selected days:", selected_days)
