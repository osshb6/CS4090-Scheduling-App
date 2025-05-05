from tkinter import ttk, BooleanVar


class EmployeePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Title label centered at the top
        title_label = ttk.Label(
            self, text="Set Your Availability", font=("Helvetica", 16)
        )
        title_label.pack(pady=20)

        # Label for instructions
        ttk.Label(self, text="Days of the week you want to work:").pack(pady=10)

        # Days of the week checkboxes
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

        for day, var in self.days.items():
            ttk.Checkbutton(self, text=day, variable=var).pack(anchor="w", padx=40)

        ttk.Button(self, text="Submit", command=self.submit_availability).pack(pady=20)

        ttk.Button(
            self, text="Sign Out", command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=20)

    def submit_availability(self):
        selected_days = [day for day, var in self.days.items() if var.get()]
        print("Selected days:", selected_days)
