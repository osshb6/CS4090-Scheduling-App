from tkinter import ttk
import random
from backend.Availability import Availability
from backend.Database import AvailabilityTable, ShiftTable, UserTable
from backend.Shift import Shift
from datetime import datetime
import tkinter as tk


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

        ttk.Button(
            center_frame,
            text="Random Valid Checks",
            style="Create.TButton",
            command=self.generate_random_schedule
        ).pack(pady=15, padx=100)

        ttk.Button(
            center_frame,
            text="Prioritize Manager Availability",
            style="Create.TButton",
            command=self.generate_managercentric_schedule
        ).pack(pady=15, padx=100)

        ttk.Button(
            center_frame,
            text="Reduce Empty Slots",
            style="Create.TButton",
            command=self.generate_optimized_schedule
        ).pack(pady=15, padx=100)

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
        ).pack(pady=15, padx=100)


    def generate_random_schedule(self):
        shifts = ShiftTable().get_all_shifts()
        availabilities = AvailabilityTable().get_all_availability()
        
        # Group shifts by day of week
        shifts_by_day = {}
        for shift in shifts:
            day = shift[2]  # day_of_week
            if day not in shifts_by_day:
                shifts_by_day[day] = []
            shifts_by_day[day].append(shift)
        
        # Process each day of week separately
        selected_shift_objects = []
        for day, day_shifts in shifts_by_day.items():
            # Get users available on this day
            users_available_on_day = set()
            user_availabilities = {}  # Store availability objects by user_id
            
            for availability in availabilities:
                if availability[2] == day:  # matching day
                    user_id = availability[1]
                    users_available_on_day.add(user_id)
                    
                    if user_id not in user_availabilities:
                        user_availabilities[user_id] = []
                    
                    availability_obj = Availability(
                        id=availability[0], 
                        user_id=user_id,
                        day_of_week=availability[2],
                        start_time=availability[3],
                        end_time=availability[4]
                    )
                    user_availabilities[user_id].append(availability_obj)
            
            # Shuffle the available users to randomize assignment
            available_users = list(users_available_on_day)
            random.shuffle(available_users)
            
            # Track which users have been assigned already for this day
            assigned_users = set()
            
            # Process each shift for this day
            for shift in day_shifts:
                shift_obj = Shift(
                    id=shift[0],
                    user_id=None,  # Will be assigned
                    day_of_week=shift[2],
                    start_time=shift[3],
                    end_time=shift[4]
                )
                
                shift_start_time = datetime.strptime(shift_obj.start_time, '%H:%M')
                shift_end_time = datetime.strptime(shift_obj.end_time, '%H:%M')
                
                # Find an unassigned user who is available for this shift
                assigned_user = None
                for user_id in available_users:
                    # Skip if already assigned to another shift this day
                    if user_id in assigned_users:
                        continue
                    
                    # Check if user's availability covers this shift
                    can_work_shift = False
                    if user_id in user_availabilities:
                        for avail in user_availabilities[user_id]:
                            avail_start = datetime.strptime(avail.start_time, '%H:%M')
                            avail_end = datetime.strptime(avail.end_time, '%H:%M')
                            
                            if avail_start <= shift_start_time and avail_end >= shift_end_time:
                                can_work_shift = True
                                break
                    
                    if can_work_shift:
                        assigned_user = user_id
                        assigned_users.add(user_id)
                        break
                
                if assigned_user:
                    shift_obj.user_id = assigned_user
                    selected_shift_objects.append(shift_obj)
        
        # Get employee names for display
        for shift in selected_shift_objects:
            if shift.user_id:
                user_info = UserTable().get_user_from_id(shift.user_id)
                # Make sure we have valid user info before assigning
                if user_info and len(user_info) > 1:
                    shift.employee = user_info[1]
                else:
                    shift.employee = f"User {shift.user_id}"
            else:
                shift.employee = "None"
        
        # Create popup window with schedule table
        popup = tk.Toplevel(self)
        popup.title("Random Valid Schedule")
        days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        columns = ("Start Time", "End Time") + days_of_week
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col.title())
        
        # Initialize schedule layout
        data = [
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None]
        ]
        
        # Fill in the schedule grid
        for shift in selected_shift_objects:
            day_index = days_of_week.index(shift.day_of_week) + 2  # +2 because first two columns are start/end times
            
            # Find the right row for this shift's time
            for row in data:
                if row[0] == shift.start_time and row[1] == shift.end_time and row[day_index] is None:
                    row[day_index] = shift.employee
                    break
        
        # Add rows to the tree view
        for row in data:
            tree.insert("", tk.END, values=row)
        
        tree.pack(padx=20, pady=10, fill="both", expand=True)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

        
    
    def generate_managercentric_schedule(self):
        shifts = ShiftTable().get_all_shifts()
        availabilities = AvailabilityTable().get_all_availability()
        
        # Get all users with their roles
        all_users = UserTable().get_all_users()
        user_roles = {}
        for user in all_users:
            user_id = user[0]
            user_role = user[3]  # Role field from the Users table
            user_roles[user_id] = user_role
        
        # Group shifts by day of week
        shifts_by_day = {}
        for shift in shifts:
            day = shift[2]  # day_of_week
            if day not in shifts_by_day:
                shifts_by_day[day] = []
            shifts_by_day[day].append(shift)
        
        # Process each day of week separately
        selected_shift_objects = []
        for day, day_shifts in shifts_by_day.items():
            # Build user availability data for this day
            users_available_on_day = []
            user_availabilities = {}  # Store availability objects by user_id
            
            for availability in availabilities:
                if availability[2] == day:  # matching day
                    user_id = availability[1]
                    
                    # Create user data structure with role info
                    user_data = {
                        'id': user_id,
                        'role': user_roles.get(user_id, 'Employee')  # Default to Employee if not found
                    }
                    users_available_on_day.append(user_data)
                    
                    if user_id not in user_availabilities:
                        user_availabilities[user_id] = []
                    
                    availability_obj = Availability(
                        id=availability[0], 
                        user_id=user_id,
                        day_of_week=availability[2],
                        start_time=availability[3],
                        end_time=availability[4]
                    )
                    user_availabilities[user_id].append(availability_obj)
            
            # Sort available users by role (Managers first)
            users_available_on_day.sort(key=lambda x: 0 if x['role'] == 'Manager' else 1)
            
            # Track which users have been assigned already for this day
            assigned_users = set()
            
            # Process each shift for this day
            for shift in day_shifts:
                shift_obj = Shift(
                    id=shift[0],
                    user_id=None,  # Will be assigned
                    day_of_week=shift[2],
                    start_time=shift[3],
                    end_time=shift[4]
                )
                
                shift_start_time = datetime.strptime(shift_obj.start_time, '%H:%M')
                shift_end_time = datetime.strptime(shift_obj.end_time, '%H:%M')
                
                # Find an unassigned user who is available for this shift
                assigned_user = None
                
                # First try to assign managers, then regular employees
                for user_data in users_available_on_day:
                    user_id = user_data['id']
                    
                    # Skip if already assigned to another shift this day
                    if user_id in assigned_users:
                        continue
                    
                    # Check if user's availability covers this shift
                    can_work_shift = False
                    if user_id in user_availabilities:
                        for avail in user_availabilities[user_id]:
                            avail_start = datetime.strptime(avail.start_time, '%H:%M')
                            avail_end = datetime.strptime(avail.end_time, '%H:%M')
                            
                            if avail_start <= shift_start_time and avail_end >= shift_end_time:
                                can_work_shift = True
                                break
                    
                    if can_work_shift:
                        assigned_user = user_id
                        assigned_users.add(user_id)
                        break
                
                if assigned_user:
                    shift_obj.user_id = assigned_user
                    selected_shift_objects.append(shift_obj)
        
        # Get employee names for display
        for shift in selected_shift_objects:
            if shift.user_id:
                user_info = UserTable().get_user_from_id(shift.user_id)
                # Make sure we have valid user info before assigning
                if user_info and len(user_info) > 1:
                    # Add role indicator for managers
                    user_role = user_roles.get(shift.user_id, 'Employee')
                    if user_role == 'Manager':
                        shift.employee = f"{user_info[1]} (M)"  # Add (M) indicator for managers
                    else:
                        shift.employee = user_info[1]
                else:
                    shift.employee = f"User {shift.user_id}"
            else:
                shift.employee = "None"
        
        # Create popup window with schedule table
        popup = tk.Toplevel(self)
        popup.title("Priority-Based Schedule (Managers First)")
        days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        columns = ("Start Time", "End Time") + days_of_week
        tree = ttk.Treeview(popup, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col.title())
        
        # Initialize schedule layout
        data = [
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None]
        ]
        
        # Fill in the schedule grid
        for shift in selected_shift_objects:
            day_index = days_of_week.index(shift.day_of_week) + 2  # +2 because first two columns are start/end times
            
            # Find the right row for this shift's time
            for row in data:
                if row[0] == shift.start_time and row[1] == shift.end_time and row[day_index] is None:
                    row[day_index] = shift.employee
                    break
        
        # Add rows to the tree view
        for row in data:
            tree.insert("", tk.END, values=row)
        
        tree.pack(padx=20, pady=10, fill="both", expand=True)
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
        
        # Add a legend for the manager indicator
        legend_frame = ttk.Frame(popup)
        legend_frame.pack(pady=5)
        ttk.Label(legend_frame, text="(M) = Manager").pack(side=tk.LEFT, padx=5)

    def generate_optimized_schedule(self):
        """Generate a schedule that minimizes the number of open shifts (no manager priority)."""
        shifts = ShiftTable().get_all_shifts()
        availabilities = AvailabilityTable().get_all_availability()
        
        all_users = UserTable().get_all_users()
        user_names = {user[0]: user[1] for user in all_users}

        shift_objects = []
        for shift in shifts:
            shift_objects.append(Shift(
                id=shift[0],
                user_id=None,
                day_of_week=shift[2],
                start_time=shift[3],
                end_time=shift[4]
            ))

        user_availabilities = {}
        for availability in availabilities:
            avail_obj = Availability(
                id=availability[0], 
                user_id=availability[1],
                day_of_week=availability[2],
                start_time=availability[3],
                end_time=availability[4]
            )
            user_availabilities.setdefault(avail_obj.user_id, []).append(avail_obj)

        def can_user_work_shift(user_id, shift):
            if user_id not in user_availabilities:
                return False
            shift_start = datetime.strptime(shift.start_time, '%H:%M')
            shift_end = datetime.strptime(shift.end_time, '%H:%M')
            for avail in user_availabilities[user_id]:
                if avail.day_of_week == shift.day_of_week:
                    avail_start = datetime.strptime(avail.start_time, '%H:%M')
                    avail_end = datetime.strptime(avail.end_time, '%H:%M')
                    if avail_start <= shift_start and avail_end >= shift_end:
                        return True
            return False

        shifts_by_day = {}
        for shift in shift_objects:
            shifts_by_day.setdefault(shift.day_of_week, []).append(shift)

        shift_user_compatibility = {}
        for shift in shift_objects:
            shift_user_compatibility[shift.id] = [
                {'user_id': user_id}
                for user_id in user_availabilities
                if can_user_work_shift(user_id, shift)
            ]

        final_assignments = {}
        for day, day_shifts in shifts_by_day.items():
            day_shift_matrix = {}
            user_shift_options = {}

            for shift in day_shifts:
                day_shift_matrix[shift.id] = []
                for user_data in shift_user_compatibility[shift.id]:
                    user_id = user_data['user_id']
                    day_shift_matrix[shift.id].append(user_id)
                    user_shift_options.setdefault(user_id, []).append(shift.id)

            assigned_users = set()
            assigned_shifts = set()

            # Prioritize users with fewest options
            remaining_users = {}
            for user_id, shift_options in user_shift_options.items():
                if user_id not in assigned_users:
                    remaining_options = [s for s in shift_options if s not in assigned_shifts]
                    if remaining_options:
                        remaining_users[user_id] = remaining_options

            sorted_users = sorted(remaining_users.items(), key=lambda x: len(x[1]))

            for user_id, available_shifts in sorted_users:
                if user_id in assigned_users:
                    continue
                unassigned_shifts = [s for s in available_shifts if s not in assigned_shifts]
                if unassigned_shifts:
                    chosen_shift = unassigned_shifts[0]
                    final_assignments[chosen_shift] = user_id
                    assigned_users.add(user_id)
                    assigned_shifts.add(chosen_shift)

            # Final pass to fill any remaining shifts
            for shift in day_shifts:
                if shift.id not in assigned_shifts:
                    for user_data in shift_user_compatibility[shift.id]:
                        user_id = user_data['user_id']
                        if user_id not in assigned_users:
                            final_assignments[shift.id] = user_id
                            assigned_users.add(user_id)
                            assigned_shifts.add(shift.id)
                            break

        for shift in shift_objects:
            if shift.id in final_assignments:
                shift.user_id = final_assignments[shift.id]
                shift.employee = user_names.get(shift.user_id, f'User {shift.user_id}')
            else:
                shift.employee = "UNASSIGNED"

        # --- GUI rendering code ---
        popup = tk.Toplevel(self)
        popup.title("Optimized Schedule (Minimum Open Shifts)")
        days_of_week = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        columns = ("Start Time", "End Time") + days_of_week
        tree = ttk.Treeview(popup, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col.title())

        data = [
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["06:00", "14:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None],
            ["14:00", "22:00", None, None, None, None, None, None, None]
        ]

        for shift in shift_objects:
            day_index = days_of_week.index(shift.day_of_week) + 2
            for row in data:
                if row[0] == shift.start_time and row[1] == shift.end_time and row[day_index] is None:
                    row[day_index] = shift.employee
                    break

        open_shifts = sum(1 for shift in shift_objects if not shift.user_id)
        total_shifts = len(shift_objects)

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(padx=20, pady=10, fill="both", expand=True)

        info_frame = ttk.Frame(popup)
        info_frame.pack(pady=5, fill="x", expand=True)

        stats_label = ttk.Label(
            info_frame, 
            text=f"Stats: {total_shifts - open_shifts}/{total_shifts} shifts filled ({open_shifts} open)"
        )
        stats_label.pack(side=tk.LEFT, padx=20)

        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
        ttk.Button(popup, text="Choose Schedule", command= lambda: self.choose_and_close(popup, data)).pack(pady=10)

    
    def choose_and_close(self, popup, data):
        self.controller.chosen_schedule = data
        popup.destroy()
