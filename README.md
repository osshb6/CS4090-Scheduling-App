# Scheduling App Project
## About the application
This is a local desktop application that makes scheduling smarter and easier. Managers can quickly build and adjust weekly schedules (along with other essential operations) based on real-time availability and role requirements, while employees can view their shifts and update their availability directly through the interface.
## Installation Instructions
1. Clone the repository to your machine
2. Optional: Set up virtual python environment for application
3. Install application dependencies from requirements.txt

Note: This application requires tkinter and sqlite3 which may not be included in the standard library of your interpreter.
## Running the Application
### First time setup
Initialize a new database for your business environment with `$ python3 src/init_blank_with_admin.py` This creates a new environment with one management account (username admin). If this command is giving errors, ensure that database/data.db does not already exist. This should only be performed once when setting up the application, not everytime the app is run. After running the application (see below), you can login with the admin account and configure your business environment as desired.
### Everyday use
Run the application with `$ python3 src/driver.py` This will take you to the login page where the application is ready to use.
## Quick Start
For detailed instructions on how to operate the application, see Documentation/user_documentation.pdf