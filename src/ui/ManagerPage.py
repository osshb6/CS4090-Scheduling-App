import sqlite3
from tkinter import messagebox, ttk
from backend.Database import UserTable
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
        ttk.Button(self, text="Promote employee", command=self.promote).pack(pady=8)

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
