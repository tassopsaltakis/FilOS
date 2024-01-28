import getpass
import hashlib
import os
import secrets
import shutil
import subprocess
import ast
import operator
import sys


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
    root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))
    home_dir = os.path.join(root_dir, 'home')
    config_dir = os.path.join(root_dir, 'config')
    users_file = os.path.join(config_dir, 'users.txt')
    groups_file = os.path.join(config_dir, 'groups.txt')
    option = args[1]
    ##we need to add an argument here that checks if a user already exsits.
    user_name = args[2]
    if option == 'adduser':
        user_path = os.path.join(home_dir, user_name)

        if not os.path.exists(user_path):
            os.makedirs(user_path)
            with open(os.path.join(user_path, "start.txt"), 'w') as start_file:
                start_file.write("Welcome to FilOS!")
            password = getpass.getpass("Enter password: ")
            password2 = getpass.getpass("Enter again: ")
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
            with open(users_file, 'a') as file:
                file.write(f"{user_name}\n")
            return "User Added"
    elif option == 'deluser':
        user_path = os.path.join(home_dir, user_name)
        if os.path.exists(user_path):
            os.remove(user_path)
        with open(users_file, "r") as f:
            lines = f.readlines()
        with open(users_file, "w") as f:
            for line in lines:
                if line.strip("\n") != user_name:
                    f.write(line)
        return "User Deleted"

def groupman(*args):
    root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))
    home_dir = os.path.join(root_dir, 'home')
    config_dir = os.path.join(root_dir, 'config')
    users_file = os.path.join(config_dir, 'users.txt')
    groups_file = os.path.join(config_dir, 'groups.txt')
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
    elif option == 'adduser': ##not done yet
        with open(groups_file, "r") as f:
            lines = f.readlines()
        with open(groups_file, "w") as f:
            for line in lines:
                if line.strip("\n") != group_name:
                    f.write(f"{group_name}")








script_dir = os.path.dirname(os.path.abspath(__file__))  # This is your current script directory (src)
root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))  # This goes up two levels to FilOS
config_dir = os.path.join(root_dir, 'config')  # This is the full path to your config directory
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
commands = load_commands_from_file(os.path.join(config_dir, 'commands.txt'))


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
