import tkinter as tk
from tkinter import ttk
from backend.TimeFrame import TimeFrame
from datetime import datetime
from backend.Database import AvailabilityTable


class UpdateAvailabilityPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # === Scrollable Frame Setup ===
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Optional: Mousewheel scrolling
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        # === Page Content ===
        self.time_options = [
            f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)
        ]

        ttk.Label(
            self.scrollable_frame, text="Update Availability", font=("Arial", 16)
        ).pack(pady=10)
        self.day_interval_frames = {}

        for day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]:
            self.create_day_section(day)

        ttk.Button(
            self.scrollable_frame,
            text="Back",
            command=lambda: controller.show_frame(
                "ManagerPage"
                if self.controller.user.title == "Manager"
                else "EmployeeDashboardPage"
            ),
        ).pack(pady=10)

    def create_day_section(self, day):
        frame = ttk.LabelFrame(self.scrollable_frame, text=day)
        frame.pack(fill="x", padx=10, pady=5)

        input_frame = ttk.Frame(frame)
        input_frame.pack(fill="x", padx=5, pady=2)

        vcmd = (
            self.register(self.validate_time),
            "%P",
            "%W",
        )

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

        intervals_frame = ttk.Frame(frame)
        intervals_frame.pack(fill="x", padx=5, pady=2)
        self.day_interval_frames[day] = intervals_frame

        add_button = ttk.Button(
            input_frame,
            text="Add",
            command=lambda: self.add_interval(
                day, start_spin.get(), end_spin.get(), intervals_frame
            ),
        )
        add_button.pack(side="left", padx=5)

    def add_interval(self, day, start, end, container, write_to_disk=True):
        if start >= end:
            return

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

        if write_to_disk:
            AvailabilityTable().add_availability(
                self.controller.user.id, day, start, end
            )

    def remove_interval(self, day, start, end, frame):
        AvailabilityTable().delete_by_day_and_time(
            self.controller.user.id, day, start, end
        )
        frame.destroy()

    def validate_time(self, value, widget_name):
        if value not in self.time_options:
            self.after(1, lambda: self.nametowidget(widget_name).delete(0, "end"))
            self.after(1, lambda: self.nametowidget(widget_name).insert(0, "00:00"))
            return False
        return True

    def on_show(self):
        for day, frame in self.day_interval_frames.items():
            for widget in frame.winfo_children():
                widget.destroy()

        availability = AvailabilityTable().get_availability_by_user(
            self.controller.user.id
        )
        for interval in availability:
            self.add_interval(
                interval[2],
                interval[3],
                interval[4],
                self.day_interval_frames[interval[2]],
                write_to_disk=False,
            )
