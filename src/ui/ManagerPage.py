import sqlite3
from tkinter import messagebox, ttk, simpledialog
from backend.Database import ShiftTable, UserTable


class ManagerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Apply styles
        style = ttk.Style()
        style.configure(
            "Manager.TLabel",
            font=("Segoe UI", 12),
            foreground="white",
            background="#333333",
        )
        style.configure("Manager.TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Make this frame fill the window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Outer frame (centered in page)
        outer_frame = ttk.Frame(self)
        outer_frame.grid(row=0, column=0)
        outer_frame.grid_columnconfigure(0, weight=1)  # Center within outer_frame

        # Center outer_frame in self
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Title
        ttk.Label(
            outer_frame,
            text="Manager Dashboard",
            style="Manager.TLabel",
            font=("Segoe UI", 16, "bold"),
        ).grid(row=0, column=0, pady=(50, 20), sticky="n")

        # Buttons
        buttons = [
            ("Add account", self.create_account),
            ("Delete account", self.delete_account),
            ("Create Shift", self.create_shift),
            ("Show Shifts", self.show_shifts),
            ("Delete Shift", self.delete_shift),
            ("Promote employee", self.promote),
            ("Create Schedules", lambda: controller.show_frame("CreateSchedulePage")),
            (
                "Change Your Availability",
                lambda: controller.show_frame("UpdateAvailabilityPage"),
            ),
            ("Show Employees", self.show_employees),
            ("Sign Out", lambda: controller.show_frame("LoginPage")),
        ]

        for i, (text, cmd) in enumerate(buttons, start=1):
            ttk.Button(
                outer_frame, text=text, style="Manager.TButton", command=cmd
            ).grid(row=i, column=0, pady=5, padx=40, sticky="ew")

    # display list of employees in database
    def show_employees(self):
        rows = UserTable().get_all_users()

        if not rows:
            messagebox.showinfo("Employees", "No employees found.")
            return

        msg_lines = [f"{row[0]}  –  {row[1]}  ({row[3]})" for row in rows]
        msg = "\n".join(msg_lines)

        messagebox.showinfo("Employees", msg)

    # add new employee to database
    def create_account(self):
        # prompts
        name = simpledialog.askstring("New account", "Username:")
        if not name:
            return
        title = simpledialog.askstring("New account", "Title / Position:")
        if not title:
            return

        role = simpledialog.askstring(
            "New account", "Role (Employee / Manager):", initialvalue="Employee"
        )
        if role is None:
            return
        role = role.strip().title() or "Employee"

        # attempt to add with error handling
        try:
            new_id = UserTable().create_user(name, title, role)
            messagebox.showinfo("Success", f"User #{new_id} – {name} ({role}) created.")
        except sqlite3.IntegrityError as err:
            messagebox.showerror("Database error", str(err))

    # remove employee from database
    def delete_account(self):
        name = simpledialog.askstring("Delete account", "Username to delete:")
        if not name:
            return

        # try to find employee
        row = UserTable().get_user(name.strip())
        if row is None:
            messagebox.showwarning("Not found", f"No user called '{name}' exists.")
            return
        user_id, _, title, role = row
        # confirm delete
        ok = messagebox.askyesno(
            "Confirm delete", f"Delete user #{user_id} – {name} ({role})?"
        )
        if not ok:
            return
        # attemp to delete with error handling
        try:
            UserTable().delete_user(name)
            messagebox.showinfo("Deleted", f"User '{name}' (id {user_id}) removed.")
        except sqlite3.DatabaseError as err:
            messagebox.showerror("Database error", str(err))

    # change employee role from employee to manager
    def promote(self):
        name = simpledialog.askstring("Promotion Page", "Username to promote:")
        if not name:
            return
        # try to find user
        row = UserTable().get_user(name.strip())
        if row is None:
            messagebox.showwarning("Not found", f"No user called '{name}' exists.")
            return
        user_id, _, title, role = row

        # promote with handling for already promoted
        if role.lower() == "manager":
            messagebox.showinfo("Already Manager", f"'{name}' is already a manager.")
            return
        ok = messagebox.askyesno(
            "Confirm promotion", f"Promote employee #{user_id} – {name} ({role})?"
        )
        if not ok:
            return
        # attempt to update in database with error handling
        try:
            UserTable().update_user(user_id, role="Manager")
            messagebox.showinfo("Promoted!!", f"Employee '{name}' (id {user_id}).")
        except sqlite3.DatabaseError as err:
            messagebox.showerror("Database error", str(err))

    # add a shift to the database
    def create_shift(self):
        # prompts
        shift_date = simpledialog.askstring("New shift", "Shift Day of the week")

        if not shift_date:
            return

        start_time = simpledialog.askstring("New shift", "Start Time (HH:MM):")
        if not start_time:
            return

        end_time = simpledialog.askstring("New shift", "End Time (HH:MM):")
        if not end_time:
            return

        role = simpledialog.askstring("New shift", "Name:", initialvalue="Fill in")
        if role is None:
            return
        role = role.strip().title() or "Fill in"

        # attempt to add with error handling
        try:
            new_shift_id = ShiftTable().create_shift(
                shift_date, start_time, end_time, role
            )
            messagebox.showinfo(
                "Success",
                f"Shift #{new_shift_id} on {shift_date} from {start_time} to {end_time} created for {role}.",
            )
        except sqlite3.IntegrityError as err:
            messagebox.showerror("Database error", str(err))

    def delete_shift(self):
        shift_id = simpledialog.askstring("Delete shift", "Enter Shift ID to delete:")
        if not shift_id:
            return

        try:
            ShiftTable().delete_shift(int(shift_id))
            messagebox.showinfo("Success", f"Shift #{shift_id} has been deleted.")
        except ValueError:
            messagebox.showerror("Input error", "Please enter a valid Shift ID.")
        except sqlite3.DatabaseError as err:
            messagebox.showerror("Database error", str(err))

    def show_shifts(self):
        rows = ShiftTable().get_all_shifts()

        if not rows:
            messagebox.showinfo("Shifts", "No shifts found.")
            return

        msg_lines = [
            f"Shift ID#{row[0]} – Day - {row[1]} – {row[2]} – {row[3]} for {row[4]}"
            for row in rows
        ]
        msg = "\n".join(msg_lines)
        messagebox.showinfo("Shifts", msg)
