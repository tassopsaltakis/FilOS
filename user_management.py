import os
import hashlib

class UserManagement:
    def __init__(self):
        # Get the absolute directory of the currently executing script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up one directory to 'root' then to 'home'
        root_dir = os.path.abspath(os.path.join(script_dir, '..'))
        self.home_dir = os.path.join(root_dir, 'home')
        self.hashes_dir = os.path.join(root_dir, 'misc', 'hashes')

    def create_user(self):
        print("\n--- Create New User ---")
        username = input("Desired username: ").strip().lower()
        real_name = input("Your full name: ").strip()

        while True:
            password = input("New password: ").strip()
            confirm_password = input("Confirm password: ").strip()
            if password == confirm_password:
                break
            else:
                print("Passwords do not match. Please try again.")

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_path = os.path.join(self.home_dir, username)

        try:
            os.makedirs(user_path, exist_ok=True)
            with open(os.path.join(user_path, "start.txt"), 'w') as start_file:
                start_file.write("Welcome to FilOS!")

            hash_file = os.path.join(self.hashes_dir, f"{username}_hash.txt")
            with open(hash_file, 'w') as f:
                f.write(hashed_password)

            print(f"\nUser {username} created successfully! Ready to login.\n")
            return username

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def login_user(self):
        print("\n--- Login ---")
        try:
            users = os.listdir(self.home_dir)
            if not users:
                print("No users found. Please create a new user first.")
                return None

            username = input("Username: ").strip().lower()
            if username in users:
                password = input("Password: ").strip()
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                hash_file = os.path.join(self.hashes_dir, f"{username}_hash.txt")
                if os.path.exists(hash_file):
                    with open(hash_file, 'r') as f:
                        stored_hash = f.read().strip()
                    if hashed_password == stored_hash:
                        print(f"Logged in as {username}. Welcome back!")
                        return username
                    else:
                        print("Incorrect password.")
                else:
                    print("User authentication data not found.")
            else:
                print("User not found.")
            return None
        except FileNotFoundError:
            print(f"Error: The specified directory {self.home_dir} does not exist.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def run(self):
        while True:
            print("\nWelcome to FilOS!")
            print("1. Login")
            print("2. Create New User")
            choice = input("Select an option (1 or 2): ").strip()
            if choice == '1':
                username = self.login_user()
                if username:  # If login is successful
                    # This is where you'd typically transition to the shell or next part of your application
                    return username  # Adjust as needed for your application's flow
            elif choice == '2':
                self.create_user()
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    user_mgmt = UserManagement()
    user_mgmt.run()
