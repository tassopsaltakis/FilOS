# Import the necessary modules for user and group management
from user_management import UserManagement

def run_login_sequence():
    """
    Run the initial login sequence for the application.
    Checks for superuser existence, creates one if necessary,
    and then proceeds with regular user login or creation.
    """
    user_mgmt = UserManagement()

    # Check and initiate superuser setup if necessary
    if not user_mgmt.superuser_exists():
        print("No superuser found. Initiating superuser creation process.")
        user_mgmt.create_superuser()

    # Handle regular login or user creation based on group-based policies
    current_user, is_superuser = user_mgmt.run()

    # Check user's group membership and apply group-based policies
    if is_superuser:
        print(f"Logged in as superuser: {current_user}")
        # Perform actions allowed for superusers
    else:
        print(f"Logged in as user: {current_user}")
        # Perform actions allowed for regular users

if __name__ == "__main__":
    # Execute the login sequence when the script is run directly
    run_login_sequence()
