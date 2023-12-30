# login.py
from user_management import UserManagement

def run_login_sequence():
    user_mgmt = UserManagement()
    current_user = user_mgmt.run()
    print(f"Logged in as: {current_user}")

if __name__ == "__main__":
    run_login_sequence()
