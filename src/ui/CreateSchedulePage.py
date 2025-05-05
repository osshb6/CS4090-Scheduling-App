from tkinter import ttk


class CreateSchedulePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        title_label = ttk.Label(self, text="Create Schedules", font=("Helvetica", 16))
        title_label.pack(pady=20)

        ttk.Button(
            self,
            text="Strategy1",
            command=lambda: print("automatically download a file of the generated schedule")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Strategy2",
            command=lambda: print("automatically download a file of the generated schedule")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Strategy3",
            command=lambda: print("automatically download a file of the generated schedule")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Sign Out",
            command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("ManagerPage")
        ).pack(pady=10)
