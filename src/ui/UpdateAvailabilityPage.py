import tkinter as tk
from tkinter import ttk
from backend.TimeFrame import TimeFrame
from datetime import datetime
from backend.Database import AvailabilityTable


class UpdateAvailabilityPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Times available in spinbox
        self.time_options = [
            f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)
        ]

        ttk.Label(self, text="Update Availability", font=("Arial", 16)).pack(pady=10)
        self.day_frames = {}

        for day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturaday",
            "Sunday",
        ]:  # create section for each day
            self.create_day_section(day)

        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame("EmployeeDashboardPage"),
        ).pack(pady=10)

    def create_day_section(self, day):
        frame = ttk.LabelFrame(self, text=day)
        frame.pack(fill="x", padx=10, pady=5)
        self.day_frames[day] = frame

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=5, pady=2)

        vcmd = (
            self.register(self.validate_time),
            "%P",
            "%W",
        )  # validation function for raw spinbox inputs

        # spin boxes
        start_spin = tk.Spinbox(
            input_frame,
            values=self.time_options,
            width=6,
            validate="focusout",
            validatecommand=vcmd,
        )
        start_spin.pack(side="left", padx=5)

        end_spin = tk.Spinbox(
            input_frame,
            values=self.time_options,
            width=6,
            validate="focusout",
            validatecommand=vcmd,
        )
        end_spin.pack(side="left", padx=5)

        add_button = ttk.Button(
            input_frame,
            text="Add",
            command=lambda: self.add_interval(
                day, start_spin.get(), end_spin.get(), intervals_frame
            ),
        )
        add_button.pack(side="left", padx=5)

        intervals_frame = ttk.Frame(frame)
        intervals_frame.pack(fill="x", padx=5, pady=2)

    def add_interval(self, day, start, end, container):
        if start >= end:
            return  # Invalid interval, do nothing for now

        frame = ttk.Frame(container)
        frame.pack(anchor="w", pady=1)

        label = ttk.Label(frame, text=f"{start} - {end}")
        label.pack(side="left")

        delete_btn = ttk.Button(
            frame,
            text="X",
            width=2,
            command=lambda: self.remove_interval(day, start, end, frame),
        )
        delete_btn.pack(side="left", padx=5)

        # add to database
        AvailabilityTable().add_availability(self.controller.user.id, day, start, end)

    def remove_interval(self, day, start, end, frame):
        # remove from database
        AvailabilityTable().delete_by_day_and_time(self.controller.user.id, start, end)
        frame.destroy()

    def validate_time(self, value, widget_name):
        if value not in self.time_options:
            self.after(1, lambda: self.nametowidget(widget_name).delete(0, "end"))
            self.after(1, lambda: self.nametowidget(widget_name).insert(0, "00:00"))
            return False
        return True
