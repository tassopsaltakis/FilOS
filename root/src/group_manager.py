import os
import hashlib
import getpass
import secrets
import commands


class GroupManagement:
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

    def groupman(groups_file, *args):
        option = args[1]
        ##we need to add an argument here that checks if a group already exsits.
        group_name = args[2]
        user_name = args[3]
        if option == 'addgroup':
            with open(groups_file, 'w') as file:
                for group_name in groups_file.groups.items():
                    file.write(f"{group_name}:\n")
        elif option == 'delgroup':
            with open(groups_file, "r") as f:
                lines = f.readlines()
            with open(groups_file, "w") as f:
                for line in lines:
                    if line.strip("\n") != group_name:
                        f.write(line)
        elif option == 'adduser':
            with open(groups_file, "r") as f:
                lines = f.readlines()
            with open(groups_file, "w") as f:
                for line in lines:
                    if line.strip("\n") != group_name:
                        f.write(f"{group_name}")

    def save_group_info(self):
        """Save group information to the groups_file."""
        with open(self.groups_file, 'w') as file:
            for group_name in self.groups.items():
                file.write(f"{group_name}:\n")


if __name__ == "__main__":
    group_mgmt = GroupManagement()
    group_mgmt.run()
