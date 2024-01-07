import os
from user_management import UserManagement
import commands
import time

class FilOSShell:
    def __init__(self):
        """Initialize the FilOS shell with root directory and user management."""
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'root'))
        self.user_mgmt = UserManagement()
        self.current_user = None
        self.current_dir = self.root_dir  # Start at root directory
        self.is_superuser = False

    def exit(self):
        print("Exiting FilOS.")
        quit(0)

    
    def update_prompt(self):
        """Update the shell prompt based on the current user and directory."""
        if self.current_user:
            relative_path = os.path.relpath(self.current_dir, self.root_dir)
            prompt_end = "$" if self.is_superuser else ":"
            current_time = time.ctime()
            purple_text = '\033[95m'
            red_text = '\033[31m'
            reset_color = '\033[0m'
            prompt = f"FilOS {purple_text}{self.current_user}{reset_color} {red_text}[{current_time}]{reset_color} ({relative_path}){prompt_end} "
            return prompt
        else:
            return "FilOS: "

    def run(self):
        """Run the shell, handling user login and command execution."""
        while True:
            user_info = self.user_mgmt.run()
            if user_info:
                self.current_user, self.is_superuser = user_info
                self.current_dir = os.path.join(self.root_dir, 'home', self.current_user)
                while True:
                    try:
                        command_line = input(self.update_prompt()).strip()
                    except EOFError:
                        self.exit()

                    if command_line:
                        self.execute_command(command_line)
                    if command_line == 'logout':
                        self.current_user = None
                        self.is_superuser = False
                        break
                    if command_line == 'exit':
                        self.exit()

    def execute_command(self, command_line):
        """Execute a command from the input line."""
        parts = command_line.split()
        command = parts[0]
        args = parts[1:]  # Arguments for the command

        # Update context if command is 'cd' and ensure current_dir is always updated
        if command == 'cd' and args:
            new_dir = commands.execute_command(command, self.current_dir, *args)
            if new_dir:  # If cd command returns a new path, update current directory
                self.current_dir = new_dir
            return

        # Execute other commands using the commands module
        try:
            commands.execute_command(command, self.current_dir, *args)
        except Exception as e:
            print(f"Error executing command {command}: {e}")

if __name__ == "__main__":
    shell = FilOSShell()
    shell.run()
