import getpass
import hashlib
import os
import secrets
import shutil
import subprocess
import ast
import operator
import sys
import common
import user_management
from access_control_commands import update_access_index_for_new_user
from access_control_directories import update_access_index_for_new_user
from common import current_user_info


def get_absolute_path(current_dir, path):
    if os.path.isabs(path):
        return os.path.normpath(path)

    return os.path.normpath(f"{current_dir}/{path}")

'''OS Commands'''

def ls(current_dir, *args):
    # figure out if the path is absolute or not
    path = get_absolute_path(current_dir, args[0].strip()) if len(args) else current_dir

    # try the path
    try:
        for entry in os.listdir(path):
            print(entry)
    except Exception as e:
        print(f"ls: cannot access '{path}': {e}")

def cd(current_dir, *args):
    new_dir = os.path.join(current_dir, args[0]) if args else current_dir
    return new_dir if os.path.isdir(new_dir) else current_dir

def pwd(current_dir, *args):
    print(current_dir)

def mkdir(current_dir, *args):
    for dirname in args:
        path = os.path.join(current_dir, dirname)
        try:
            os.makedirs(path)
            print(f"Directory '{dirname}' created.")
        except Exception as e:
            print(f"mkdir: cannot create directory '{dirname}': {e}")

def rmdir(current_dir, *args):
    for dirname in args:
        path = os.path.join(current_dir, dirname)
        try:
            os.rmdir(path)
            print(f"Directory '{dirname}' removed.")
        except Exception as e:
            print(f"rmdir: failed to remove '{dirname}': {e}")

def touch(current_dir, *args):
    for filename in args:
        path = os.path.join(current_dir, filename)
        try:
            open(path, 'a').close()
            os.utime(path, None)
            print(f"File '{filename}' touched.")
        except Exception as e:
            print(f"touch: cannot touch '{filename}': {e}")

def cat(current_dir, *args):
    for filename in args:
        path = os.path.join(current_dir, filename)
        try:
            with open(path, 'r') as file:
                print(file.read())
        except Exception as e:
            print(f"cat: cannot open '{filename}': {e}")

def rm(current_dir, *args):
    for filename in args:
        path = os.path.join(current_dir, filename)
        try:
            os.remove(path)
            print(f"File '{filename}' removed.")
        except Exception as e:
            print(f"rm: cannot remove '{filename}': {e}")

def cp(current_dir, *args):
    if len(args) == 2:
        source, destination = os.path.join(current_dir, args[0]), os.path.join(current_dir, args[1])
        try:
            shutil.copy(source, destination)
            print(f"Copied '{args[0]}' to '{args[1]}'.")
        except Exception as e:
            print(f"cp: cannot copy '{args[0]}': {e}")

def mv(current_dir, *args):
    if len(args) == 2:
        source, destination = os.path.join(current_dir, args[0]), os.path.join(current_dir, args[1])
        try:
            shutil.move(source, destination)
            print(f"Moved '{args[0]}' to '{args[1]}'.")
        except Exception as e:
            print(f"mv: cannot move '{args[0]}': {e}")

def pad(current_dir, *args):
    if args:
        filename = os.path.join(current_dir, args[0])  # Assumes args[0] is the filename
        pad_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'root', 'misc', 'pad', 'pad.py'))
        subprocess.run(['python', pad_path, filename])
    else:
        print("Usage: pad filename")

def calc(current_dir, *args):
    expression = ''.join(args)  # Joining args as the expression might be split into several arguments
    allowed_operators = {
        ast.Add: operator.add, 
        ast.Sub: operator.sub, 
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,  
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
    }
    def evaluate_expression(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return allowed_operators[type(node.op)](evaluate_expression(node.left), evaluate_expression(node.right))
        else:
            raise TypeError(node)

    try:
        # Safely parse the expression
        node = ast.parse(expression, mode='eval').body
        result = evaluate_expression(node)
        print(result)
    except Exception as e:
        print(f"Error calculating expression: {e}")

def pip(current_dir, *args):
    if args:
        pip_command = args[0]
        ad_argument = args[1]
        if pip_command in 'install':
            subprocess.check_call([sys.executable, "-m", "pip", pip_command, ad_argument])


    else:
        print("Usage: pip [command] [additional arguments if needed]")



'''User and Group Management'''


def userman(*args):
    user_mgmt = user_management.UserManagement()  # Instantiate the UserManagement class
    option = args[1]
    if option == 'adduser':
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        password2 = getpass.getpass("Enter again: ")

        if password != password2:
            print("Passwords didn't match. Please try again.")
        else:
            user_mgmt.create_user(username, password)  # Call create_user on the instance
            return "User Added"

    elif option == 'deluser':
        username = input("Enter username: ")
        user_path = os.path.join(common.home_dir, username)
        if os.path.exists(user_path):
            shutil.rmtree(user_path)  # Corrected to remove directory

        with open(common.users_file, "r") as f:
            lines = f.readlines()
        with open(common.users_file, "w") as f:
            for line in lines:
                if line.strip("\n") != username:
                    f.write(line)
        return "User Deleted"


def groupman(*args):
    option = args[1]

    if option == 'addgroup':
        group_name = input("Enter Group Name: ")
        with open(common.groups_file, 'r') as file:
            groups = file.read()
            if group_name + ':' in groups:
                print(f"Group '{group_name}' already exists.")
                return

        with open(common.groups_file, 'a') as file:
            file.write(f"\n{group_name}:")

    elif option == 'delgroup':
        group_name = input("Enter Group Name: ")
        with open(common.groups_file, "r") as f:
            lines = f.readlines()
        with open(common.groups_file, "w") as f:
            for line in lines:
                if line.strip("\n") != f"{group_name}:":
                    f.write(line)

    elif option == 'adduser':
        user_name = input("Enter User to add: ")
        group_name = input("Enter which group to add " +user_name+ " to: ")
        updated_groups = []
        group_found = False

        with open(common.groups_file, "r") as f:
            for line in f:
                if line.startswith(group_name + ":"):
                    group_found = True
                    if user_name not in line:
                        line = line.strip() + f" {user_name}\n"  # Append the user to the group
                updated_groups.append(line)

        if not group_found:
            print(f"Group '{group_name}' does not exist.")
            return

        with open(common.groups_file, "w") as f:
            f.writelines(updated_groups)

def sysset(*args):
    file_path = os.path.join(common.config_dir, "colorCodes.txt")
    option = args[0]
    second_option = args[1]
    if option == 'customize':
        print("========================")
        print("Customization Settings")
        print("========================")
        print("1. Appearance")
        print("")
        common.config_dir
        with open(file_path, 'r') as file:
            for line in file:
                index, data = line.strip().split(':', 1)
                if index == second_option:
                    return data
        return "Color not found"







# New function to load commands from file
def load_commands_from_file(file_path):
    command_map = {}
    with open(file_path, 'r') as file:
        for line in file.readlines():
            parts = line.strip().split(',')  # Assuming the file has lines like "ls,ls"
            if len(parts) == 2:
                cmd, func_name = parts
                if func_name in globals():  # Check if the function name exists in the global namespace
                    command_map[cmd] = globals()[func_name]
    return command_map

# Load commands from the commands.txt file
commands = load_commands_from_file(os.path.join(common.config_dir, 'commands.txt'))


# Function to execute commands based on the command name
def execute_command(command_name, *args):
    if command_name in commands:
        try:
            # If the command function returns a value, it could be handled here (e.g., new current directory from cd)
            return commands[command_name](*args)
        except Exception as e:
            print(f"Error executing command '{command_name}': {e}")
    else:
        print(f'Command "{command_name}" not recognized.')

# Example usage (this part would typically be in your main shell script):
if __name__ == '__main__':
    # Simulate user input
    user_input = "ls"
    execute_command(user_input)

    # Simulate changing directory
    new_dir = execute_command("cd", "/", "some_directory")
    if new_dir:
        print(f"Changed directory to {new_dir}")
