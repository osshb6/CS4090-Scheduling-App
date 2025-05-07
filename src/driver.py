#!/usr/bin/python3
import argparse
from backend.Database import DatabaseConnection
from ui.UI import App
from backend.Database import DatabaseConnection


parser = argparse.ArgumentParser()
parser.add_argument("--db_path", required=False)
args = parser.parse_args()

if args.db_path:
    db = DatabaseConnection(db_path=args.db_path)
else:
    db = DatabaseConnection()
app = App()
app.mainloop()
