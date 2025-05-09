#!/usr/bin/python3
"""
This script sets up a database with only a manager account called admin. This is
intended to be a starting point to build your scheduling operations from (add
employees, shifts, availability, etc.).
"""
from backend.Database import (
    DatabaseConnection,
    UserTable,
)


DatabaseConnection(db_path="database/data.db")
UserTable().create_user("admin", "Manager", "Manager")
