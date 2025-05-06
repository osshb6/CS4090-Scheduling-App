from tkinter import ttk


class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        title_label = ttk.Label(self, text="Company Settings", font=("Helvetica", 16))
        title_label.pack(pady=20)

        ttk.Button(
            self,
            text="Get employees",
            command=lambda: print("call db functions and print somewhere"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Delete employee",
            command=lambda: print("call db functions and print somewhere"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Promote employee",
            command=lambda: print("call db functions and print somewhere"),
        ).pack(pady=10)

        ttk.Button(
            self, text="Sign Out", command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=10)

        ttk.Button(
            self, text="Back", command=lambda: controller.show_frame("ManagerPage")
        ).pack(pady=10)
