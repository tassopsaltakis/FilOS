import os
import hashlib
import getpass
import secrets
import common
from common import current_user_info
from common import home_dir

class UserManagement:

    def __init__(self):
        """Set up directories for user home and configuration files."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))
        self.home_dir = os.path.join(root_dir, 'home')
        self.config_dir = os.path.join(root_dir, 'config')
        self.users_file = os.path.join(self.config_dir, 'users.txt')
        self.groups_file = os.path.join(self.config_dir, 'groups.txt')

        os.makedirs(self.config_dir, exist_ok=True)

        # Initialize user and group information dictionaries
        self.users = {}
        self.groups = {}

        # Load user and group information from files
        self.load_user_info()
        self.load_group_info()

    def load_user_info(self):
        """Load user information from the users_file."""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as file:
                for username in file:
                    username = username.strip()
                    access_path = os.path.join(self.home_dir, username, "user_data", "access.txt")
                    if os.path.exists(access_path):
                        with open(access_path, 'r') as access_file:
                            password_hash, password_salt = access_file.read().strip().split(',')
                        self.users[username] = {'password': password_hash, 'salt': password_salt}

    def load_group_info(self):
        """Load group information from the groups_file."""
        if os.path.exists(self.groups_file):
            with open(self.groups_file, 'r') as file:
                for line in file:
                    group_name, members = line.strip().split(':')
                    self.groups[group_name] = members.split(',')

    def save_group_info(self):
        """Save group information to the groups_file."""
        with open(self.groups_file, 'w') as file:
            for group_name, members in self.groups.items():
                member_list = ','.join(members)
                file.write(f"{group_name}:{member_list}\n")

    def create_user(self, username, password, is_superuser=False):
        """create the user group for group based access"""

        group_name = username

        group_found = False  # Initialize a flag to track if the group is found

        # Read the file and store lines
        with open(common.groups_file, "r") as f:
            lines = f.readlines()

        # Modify lines as needed
        with open(common.groups_file, "w") as f:
            for line in lines:
                parts = line.strip().split(":", 1)
                if len(parts) == 2:
                    current_group_name, users = parts
                    if current_group_name == group_name:
                        group_found = True
                        if username not in users.split():
                            # Append the user to the group and add newline for file writing
                            line = f"{group_name}:{users} {username}"
                f.write(line)

        if not group_found:
            # Correctly append the new group to the file
            with open(common.groups_file, 'a') as f:  # Use 'a' mode for appending
                f.write(f"{group_name}:{username}\n")  # Append the new group with the username
        user_path = os.path.join(self.home_dir, username)

        if not os.path.exists(user_path):
            os.makedirs(user_path)
            with open(os.path.join(user_path, "start.txt"), 'w') as start_file:
                start_file.write("Welcome to FilOS!")

            # Salt, hash and save the password
            password_salt = secrets.token_urlsafe(32)
            salted_password = (password + password_salt).encode()
            hashed_password = hashlib.sha256(salted_password).hexdigest()

            # Save password hash and salt in the user's access.txt file
            user_data_path = os.path.join(user_path, "user_data")
            os.makedirs(user_data_path, exist_ok=True)
            with open(os.path.join(user_data_path, "access.txt"), 'w') as access_file:
                access_file.write(f"{hashed_password},{password_salt}\n")


            # Update user list in users.txt
            with open(self.users_file, 'a') as file:
                file.write(f"\n{username}")

            # Add user to groups and create home directory
            if is_superuser:
                self.add_user_to_group(username, 'superuser')
            self.add_user_to_group(username, 'user')

            print(f"\n{'Superuser' if is_superuser else 'User'} {username} created successfully! Ready to login.\n")
            new_user_directory = os.path.join("home", username)
        else:
            print(f"\nUser '{username}' already exists.\n")

    def is_user_in_superuser_group(self, username):
        """Check if a user is in the superuser group."""
        with open(self.groups_file, 'r') as file:
            for line in file:
                group_name, members = line.strip().split(':', 1)
                if group_name == 'superuser' and username in members.split():
                    return True
        return False
    def login_user(self, username, password):
        """Authenticate a user and check group-based permissions."""
        user_data_path = os.path.join(self.home_dir, username, "user_data", "access.txt")
        if os.path.exists(user_data_path):
            with open(user_data_path, 'r') as user_data_file:
                stored_password_hash, stored_salt = user_data_file.read().strip().split(',')

            if hashlib.sha256((password + stored_salt).encode()).hexdigest() == stored_password_hash:
                print(f"Logged in as {username}. Welcome back!")
                return username, self.is_superuser(username)
            else:
                print("Incorrect password.")
        else:
            print("User authentication data not found.")
        return None
    def is_superuser(self, username):
        """Check if the given username corresponds to a superuser."""
        return self.user_in_group(username, 'superuser')

    def superuser_exists(self):
        """Check if a superuser has been set up."""
        return 'superuser' in self.users

    def create_superuser(self, username, password):
        """Initiate the superuser creation process if no superuser exists."""
        if not self.superuser_exists():
            self.create_user(username, password, is_superuser=True)
            print("\nSuperuser created successfully!\n")

    def add_user_to_group(self, username, group_name):
        """Add a user to a group."""
        if group_name not in self.groups:
            self.groups[group_name] = []
        if username not in self.groups[group_name]:
            self.groups[group_name].append(username)

    def user_in_group(self, username, group_name):
        """Check if a user is in a group."""
        return username in self.groups.get(group_name, [])


    def run(self):
        if not self.superuser_exists():
            print("No superuser found. Setting up now.")
            superuser_password = getpass.getpass("Enter superuser password: ")
            self.create_superuser('superuser', superuser_password)
        while True:
            print("\nWelcome to FilOS!")
            print("1. Login")
            print("2. Create New User")
            choice = input("Select an option (1 or 2): ").strip()
            if choice == '1':
                username = input("Enter username: ")
                password = getpass.getpass("Enter password: ")
                user_info = self.login_user(username, password)
                if user_info:  # After successful login
                    username, is_superuser = user_info
                    global current_user_info
                    current_user_info['username'] = username
                    current_user_info['is_superuser'] = is_superuser
                    return username, is_superuser
            elif choice == '2':
                username = input("Enter username: ")
                password = getpass.getpass("Enter password: ")
                password2 = getpass.getpass("Enter again: ")

                if password != password2:
                    print("Passwords didn't match. Please try again.")
                
                else:

                    self.create_user(username, password)
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    user_mgmt = UserManagement()
    user_mgmt.run()
