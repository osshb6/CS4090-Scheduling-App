#!/usr/bin/python3
"""
this is the main driver for the applicaton. it connects to the database specified by --db_path, defaulting
to database/data.db. Assumes at least one manager account already exists in the database. To create a new
database at database/data.db with only a manager account (username admin), run init_blank_with_admin.py
"""
import argparse
from backend.Database import DatabaseConnection
from ui.UI import App
from backend.Database import DatabaseConnection

# get argument
parser = argparse.ArgumentParser()
parser.add_argument("--db_path", required=False)
args = parser.parse_args()

# connect to specified db or default
if args.db_path:
    db = DatabaseConnection(db_path=args.db_path)
else:
    db = DatabaseConnection()  # defaults to data.db
# main app loop
app = App()
app.mainloop()
