import sqlite3
from tkinter import messagebox, ttk
from backend.Database import ShiftTable, UserTable
from tkinter import messagebox, simpledialog

class ManagerPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Top-center label
        title_label = ttk.Label(self, text="Manager Dashboard", font=("Helvetica", 16))
        title_label.pack(pady=20)

        ttk.Button(self, text="Add account", command=self.create_account).pack(pady=8)
        ttk.Button(self, text="Delete account", command=self.delete_account).pack(
            pady=8
        )

        ttk.Button(self, text="Create Shift", command=self.create_shift).pack(
            pady=8
        )

        ttk.Button(self, text="Show Shifts", command=self.show_shifts).pack(
            pady=8
        )

        ttk.Button(self, text="Delete Shift", command=self.delete_shift).pack(
            pady=8
        )

        ttk.Button(self,text="Promote employee", command=self.promote).pack(pady=8)

        ttk.Button(
            self,
            text="Create Schedules",
            command=lambda: controller.show_frame("CreateSchedulePage"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Change Your Availability",
            command=lambda: controller.show_frame("EmployeePage"),
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Show Employees",
            command=self.show_employees,
        ).pack(pady=10)

        ttk.Button(
            self, text="Sign Out", command=lambda: controller.show_frame("LoginPage")
        ).pack(pady=10)

    def show_employees(self):
        rows = UserTable().get_all_users()

        if not rows:
            messagebox.showinfo("Employees", "No employees found.")
            return

        msg_lines = [f"{row[0]}  –  {row[1]}  ({row[3]})" for row in rows]
        msg = "\n".join(msg_lines)

        messagebox.showinfo("Employees", msg)

    def create_account(self):
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

        try:
            new_id = UserTable().create_user(name, title, role)
            messagebox.showinfo("Success", f"User #{new_id} – {name} ({role}) created.")
        except sqlite3.IntegrityError as err:
            messagebox.showerror("Database error", str(err))

    def delete_account(self):
        name = simpledialog.askstring("Delete account", "Username to delete:")
        if not name:
            return

        row = UserTable().get_user(name.strip())
        if row is None:
            messagebox.showwarning("Not found", f"No user called '{name}' exists.")
            return
        user_id, _, title, role = row
        ok = messagebox.askyesno(
            "Confirm delete", f"Delete user #{user_id} – {name} ({role})?"
        )
        if not ok:
            return
        try:
            UserTable().delete_user(name)
            messagebox.showinfo("Deleted", f"User '{name}' (id {user_id}) removed.")
        except sqlite3.DatabaseError as err:
            messagebox.showerror("Database error", str(err))

    def promote(self):
        name = simpledialog.askstring("Promotion Page", "Username to promote:")
        if not name:
            return
        row = UserTable().get_user(name.strip())
        if row is None:
            messagebox.showwarning("Not found", f"No user called '{name}' exists.")
            return
        user_id, _, title, role = row

        if role.lower() == "manager":
            messagebox.showinfo("Already Manager", f"'{name}' is already a manager.")
            return
        ok = messagebox.askyesno(
            "Confirm promotion", f"Promote employee #{user_id} – {name} ({role})?"
        )
        if not ok:
            return
        try:
            UserTable().update_user(user_id, role="Manager")
            messagebox.showinfo("Promoted!!", f"Employee '{name}' (id {user_id}).")
        except sqlite3.DatabaseError as err:
            messagebox.showerror("Database error", str(err))


    def create_shift(self):
        shift_date = simpledialog.askstring("New shift", "Shift Day of the week")

        if not shift_date:
            return

        start_time = simpledialog.askstring("New shift", "Start Time (HH:MM):")
        if not start_time:
            return

        end_time = simpledialog.askstring("New shift", "End Time (HH:MM):")
        if not end_time:
            return

        role = simpledialog.askstring(
            "New shift", "Name:", initialvalue="Fill in"
        )
        if role is None:
            return
        role = role.strip().title() or "Fill in"

        try:
            new_shift_id = ShiftTable().create_shift(shift_date, start_time, end_time, role)
            messagebox.showinfo("Success", f"Shift #{new_shift_id} on {shift_date} from {start_time} to {end_time} created for {role}.")
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





