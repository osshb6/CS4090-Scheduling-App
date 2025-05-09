import tkinter as tk
from tkinter import ttk
from backend.TimeFrame import TimeFrame
from backend.Database import AvailabilityTable


class UpdateAvailabilityPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # valid time strings for availability start/stop
        self.time_options = [
            f"{h:02}:{m:02}" for h in range(24) for m in (0, 15, 30, 45)
        ]

        # title
        ttk.Label(self, text="Update Availability", font=("Arial", 16)).pack(
            pady=(10, 0)
        )

        # notebook stuff for tabs
        notebook_container = ttk.Frame(self)
        notebook_container.place(relx=0.5, rely=0.45, anchor="center")  # Centered box

        self.notebook = ttk.Notebook(notebook_container)
        self.notebook.pack()

        self.day_interval_frames = {}

        # create tab for each dat of week
        for day in [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]:
            self.create_day_tab(day)

        # back button
        ttk.Button(
            self,
            text="Back",
            command=lambda: controller.show_frame(
                "ManagerPage"
                if self.controller.user.title == "Manager"
                else "EmployeeDashboardPage"
            ),
        ).place(relx=0.5, rely=0.95, anchor="s")

    def create_day_tab(self, day):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=day)

        # input spinboxes
        input_frame = ttk.Frame(tab)
        input_frame.pack(pady=10, anchor="center")

        # validation function for boxes
        vcmd = (self.register(self.validate_time), "%P", "%W")

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

        # frame for showing availability to user
        intervals_frame = ttk.Frame(tab)
        intervals_frame.pack(fill="x", padx=10, pady=5)

        # make accessible to other parts of program
        self.day_interval_frames[day] = intervals_frame

        # add button to insert specified availability to UI and database
        ttk.Button(
            input_frame,
            text="Add",
            command=lambda: self.add_interval(
                day, start_spin.get(), end_spin.get(), intervals_frame
            ),
        ).pack(side="left", padx=5)

    # (optionally) add to database and create frame to show it
    def add_interval(self, day, start, end, container, write_to_disk=True):
        # check valid interval
        if start >= end:
            return

        # construct and show frame
        frame = ttk.Frame(container)
        frame.pack(anchor="w", pady=2)

        label = ttk.Label(frame, text=f"{start} - {end}")
        label.pack(side="left")

        # remove button
        ttk.Button(
            frame,
            text="X",
            width=2,
            command=lambda: self.remove_interval(day, start, end, frame),
        ).pack(side="left", padx=5)

        # optionally update database (want to do on adding new intervals, but not restoring)
        if write_to_disk:
            AvailabilityTable().add_availability(
                self.controller.user.id, day, start, end
            )

    # remove availability from database and destroy corresponding frame
    def remove_interval(self, day, start, end, frame):
        AvailabilityTable().delete_by_day_and_time(
            self.controller.user.id, day, start, end
        )
        frame.destroy()

    # sets spinboxes to default values if invalid string was entered
    def validate_time(self, value, widget_name):
        if value not in self.time_options:
            self.after(1, lambda: self.nametowidget(widget_name).delete(0, "end"))
            self.after(1, lambda: self.nametowidget(widget_name).insert(0, "00:00"))
            return False
        return True

    def on_show(self):
        # destroy previously existing widgets
        for frame in self.day_interval_frames.values():
            for widget in frame.winfo_children():
                widget.destroy()

        # get latest availability from database
        availability = AvailabilityTable().get_availability_by_user(
            self.controller.user.id
        )

        # add_interval for each availability
        for interval in availability:
            self.add_interval(
                interval[2],
                interval[3],
                interval[4],
                self.day_interval_frames[interval[2]],
                write_to_disk=False,
            )
