# Import necessary modules
from user_management import UserManagement
import os

def run_login_sequence():
    user_mgmt = UserManagement()

    # Check and initiate superuser setup if necessary
    if not user_mgmt.superuser_exists():
        print("No superuser found. Initiating superuser creation process.")
        user_mgmt.create_superuser()

    # Handle regular login or user creation based on group-based policies
    current_user, is_superuser = user_mgmt.run()

    # Set the directory for the user
    if is_superuser:
        os.chdir(user_mgmt.root_dir)  # Change directory to root for superuser
        print(f"Logged in as superuser: {current_user}")
    else:
        user_home = os.path.join(user_mgmt.home_dir, current_user)
        os.makedirs(user_home, exist_ok=True)  # Ensure user home directory exists
        os.chdir(user_home)  # Change directory to home for regular user
        print(f"Logged in as user: {current_user}")

    # Your code for launching the shell or next steps goes here
    # ...

if __name__ == "__main__":
    run_login_sequence()
