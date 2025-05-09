#!/usr/bin/python3
from backend.Database import (
    DatabaseConnection,
    UserTable,
)


DatabaseConnection(db_path="database/data.db")
UserTable().create_user("admin", "Manager", "Manager")
