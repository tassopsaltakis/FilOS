# shell.py
import os
from user_management import UserManagement
import commands

class FilOSShell:
    def __init__(self):
        self.root_dir = "..\\root"  # Use double backslashes for escape sequence
        self.user_mgmt = UserManagement()
        self.current_user = None
        self.current_dir = self.root_dir

    def update_prompt(self):
        if self.current_user:
            relative_path = os.path.relpath(self.current_dir, self.root_dir)
            return f"FilOS {self.current_user} ({relative_path}): "
        else:
            return "FilOS: "

    def run(self):
        while True:
            self.current_user = self.user_mgmt.run()
            if self.current_user:
                self.current_dir = os.path.join(self.user_mgmt.home_dir, self.current_user)
                while True:
                    command_line = input(self.update_prompt()).strip()
                    if command_line:
                        self.execute_command(command_line)
                    if command_line == 'logout':
                        self.current_user = None
                        break
                    if command_line == 'exit':
                        print("Exiting FilOS.")
                        return

    def execute_command(self, command_line):
        parts = command_line.split()
        command = parts[0]
        args = parts[1:]
        command_function = getattr(commands, command, None)
        if command_function:
            try:
                result = command_function(self.current_dir, *args)
                if command == 'cd':
                    self.current_dir = result  # Update the shell's current directory
            except TypeError as e:
                print(f"Error executing command {command}: {e}")

    

if __name__ == "__main__":
    shell = FilOSShell()
    shell.run()
