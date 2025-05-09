import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import tkinter as tk
from unittest.mock import patch, Mock
from src.ui.ManagerPage import ManagerPage


class TestUserShiftManagement(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.mock_controller = Mock()
        self.ui = ManagerPage(self.root, self.mock_controller)

    def tearDown(self):
        self.root.destroy()

    @patch("src.ui.ManagerPage.simpledialog.askstring")
    @patch("src.ui.ManagerPage.messagebox.showinfo")
    @patch("backend.Database.UserTable.create_user")
    def test_create_account_success(
        self, mock_create_user, mock_showinfo, mock_askstring
    ):
        mock_askstring.side_effect = ["john_doe", "Developer", "Employee"]
        mock_create_user.return_value = 101

        self.ui.create_account()

        mock_create_user.assert_called_with("john_doe", "Developer", "Employee")
        mock_showinfo.assert_called_once()

    @patch("src.ui.ManagerPage.simpledialog.askstring")
    @patch("src.ui.ManagerPage.messagebox.showwarning")
    @patch("backend.Database.UserTable.get_user")
    def test_delete_account_user_not_found(
        self, mock_get_user, mock_showwarning, mock_askstring
    ):
        mock_askstring.return_value = "unknown_user"
        mock_get_user.return_value = None

        self.ui.delete_account()

        mock_get_user.assert_called_with("unknown_user")
        mock_showwarning.assert_called_once()

    @patch("src.ui.ManagerPage.simpledialog.askstring")
    @patch("src.ui.ManagerPage.messagebox.showinfo")
    @patch("src.ui.ManagerPage.messagebox.askyesno")
    @patch("backend.Database.UserTable.get_user")
    @patch("backend.Database.UserTable.update_user")
    def test_promote_success(
        self,
        mock_update_user,
        mock_get_user,
        mock_askyesno,
        mock_showinfo,
        mock_askstring,
    ):
        mock_askstring.return_value = "jane_doe"
        mock_get_user.return_value = (3, "jane_doe", "Assistant", "Employee")
        mock_askyesno.return_value = True

        self.ui.promote()

        mock_update_user.assert_called_with(3, role="Manager")
        mock_showinfo.assert_called_once()

    @patch("src.ui.ManagerPage.simpledialog.askstring")
    @patch("src.ui.ManagerPage.messagebox.showinfo")
    @patch("backend.Database.ShiftTable.create_shift")
    def test_create_shift_success(
        self, mock_create_shift, mock_showinfo, mock_askstring
    ):
        mock_askstring.side_effect = ["Monday", "09:00", "17:00", "Alice"]
        mock_create_shift.return_value = 10

        self.ui.create_shift()

        mock_create_shift.assert_called_with("Monday", "09:00", "17:00", "Alice")
        mock_showinfo.assert_called_once()

    @patch("src.ui.ManagerPage.messagebox.showinfo")
    @patch("backend.Database.ShiftTable.get_all_shifts")
    def test_show_shifts(self, mock_get_all_shifts, mock_showinfo):
        mock_get_all_shifts.return_value = [
            (1, "Monday", "09:00", "17:00", "Alice"),
            (2, "Tuesday", "10:00", "18:00", "Bob"),
        ]

        self.ui.show_shifts()

        expected_msg = (
            "Shift ID#1 – Day - Monday – 09:00 – 17:00 for Alice\n"
            "Shift ID#2 – Day - Tuesday – 10:00 – 18:00 for Bob"
        )
        mock_showinfo.assert_called_with("Shifts", expected_msg)


if __name__ == "__main__":
    unittest.main()
