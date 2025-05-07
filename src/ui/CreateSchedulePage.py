from tkinter import ttk

class CreateSchedulePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Apply consistent styling
        style = ttk.Style()
        style.configure("Create.TLabel", font=("Segoe UI", 12), foreground="white", background="#333333")
        style.configure("Create.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Center content in the middle of the screen
        center_frame = ttk.Frame(self)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        ttk.Label(center_frame, text="Create Schedules", style="Create.TLabel",
                  font=("Segoe UI", 16, "bold")).pack(pady=(0, 20))

        # Strategy buttons
        for strategy in ["Strategy1", "Strategy2", "Strategy3"]:
            ttk.Button(
                center_frame,
                text=strategy,
                style="Create.TButton",
                command=lambda s=strategy: print(
                    f"{s}: automatically download a file of the generated schedule"
                )
            ).pack(pady=10, padx=100)

        # Sign Out button
        ttk.Button(
            center_frame,
            text="Sign Out",
            style="Create.TButton",
            command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=15, padx=100)

        # Back to Manager Page button
        ttk.Button(
            center_frame,
            text="Back",
            style="Create.TButton",
            command=lambda: controller.show_frame("ManagerPage")
        ).pack(pady=5, padx=100)
