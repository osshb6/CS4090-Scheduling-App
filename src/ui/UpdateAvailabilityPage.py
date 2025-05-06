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
        self.availability = {  # maps day string to list of available time frames
            day: []
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

        for day in self.availability.keys():  # create section for each day
            self.create_day_section(day)

        # save availability
        ttk.Button(
            self, text="Save and Exit", command=lambda: self.save_and_exit()
        ).pack(pady=10)
        ttk.Button(
            self,
            text="Cancel",
            command=lambda: controller.show_frame("EmployeeDashboardPage"),
        ).pack(pady=10)

    # clears current availability for user and inserts the new lists from self.availability
    def save_and_exit(self):
        AvailabilityTable().delete_by_user(self.controller.user.id)

        for day, time_frames in self.availability.items():
            for frame in time_frames:
                AvailabilityTable().add_availability(
                    self.controller.user.id,
                    day,
                    frame.start_time.strftime("%H:%M"),
                    frame.end_time.strftime("%H:%M"),
                )
        self.controller.show_frame("EmployeeDashboardPage")

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

        interval = TimeFrame(
            datetime.strptime(start, "%H:%M").time(),
            datetime.strptime(end, "%H:%M").time(),
        )
        self.availability[day].append(interval)

        frame = ttk.Frame(container)
        frame.pack(anchor="w", pady=1)

        label = ttk.Label(frame, text=f"{start} - {end}")
        label.pack(side="left")

        delete_btn = ttk.Button(
            frame,
            text="X",
            width=2,
            command=lambda: self.remove_interval(day, interval, frame),
        )
        delete_btn.pack(side="left", padx=5)

    def remove_interval(self, day, interval, frame):
        if interval in self.availability[day]:
            self.availability[day].remove(interval)
            frame.destroy()

    def validate_time(self, value, widget_name):
        if value not in self.time_options:
            self.after(1, lambda: self.nametowidget(widget_name).delete(0, "end"))
            self.after(1, lambda: self.nametowidget(widget_name).insert(0, "00:00"))
            return False
        return True
