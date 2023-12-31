import os
import hashlib

class UserManagement:
    def __init__(self):
        """Set up directories for user home and configuration files."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'root'))
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
                for line in file:
                    username, password_hash = line.strip().split(',')
                    self.users[username] = {'password': password_hash}

    def load_group_info(self):
        """Load group information from the groups_file."""
        if os.path.exists(self.groups_file):
            with open(self.groups_file, 'r') as file:
                for line in file:
                    group_name, members = line.strip().split(':')
                    self.groups[group_name] = members.split(',')

    def save_user_info(self):
        """Save user information to the users_file."""
        with open(self.users_file, 'w') as file:
            for username, user_info in self.users.items():
                password_hash = user_info['password']
                file.write(f"{username},{password_hash}\n")

    def save_group_info(self):
        """Save group information to the groups_file."""
        with open(self.groups_file, 'w') as file:
            for group_name, members in self.groups.items():
                member_list = ','.join(members)
                file.write(f"{group_name}:{member_list}\n")

    def create_user(self, username, password, is_superuser=False):
        """Create a new user, assign them to groups, and create a home directory."""
        user_path = os.path.join(self.home_dir, username)

        if not os.path.exists(user_path):
            os.makedirs(user_path)
            with open(os.path.join(user_path, "start.txt"), 'w') as start_file:
                start_file.write("Welcome to FilOS!")

            # Hash and save the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.users[username] = {'password': hashed_password}

            # Add user to groups and create home directory
            if is_superuser:
                self.add_user_to_group(username, 'superuser')
            self.add_user_to_group(username, 'user')

            # Save user information
            self.save_user_info()
            self.save_group_info()

            print(f"\n{'Superuser' if is_superuser else 'User'} {username} created successfully! Ready to login.\n")
        else:
            print(f"\nUser '{username}' already exists.\n")

    def login_user(self, username, password):
        """Authenticate a user and check group-based permissions."""
        if username in self.users and 'password' in self.users[username]:
            stored_password = self.users[username]['password']
            if hashlib.sha256(password.encode()).hexdigest() == stored_password:
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
            superuser_password = input("Enter superuser password: ")
            self.create_superuser('superuser', superuser_password)
        while True:
            print("\nWelcome to FilOS!")
            print("1. Login")
            print("2. Create New User")
            choice = input("Select an option (1 or 2): ").strip()
            if choice == '1':
                username = input("Enter username: ")
                password = input("Enter password: ")
                user_info = self.login_user(username, password)
                if user_info:
                    username, is_superuser = user_info
                    return username, is_superuser
            elif choice == '2':
                username = input("Enter username: ")
                password = input("Enter password: ")
                self.create_user(username, password)
            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    user_mgmt = UserManagement()
    user_mgmt.run()
