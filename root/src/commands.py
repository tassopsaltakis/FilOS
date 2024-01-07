import os
import shutil
import subprocess
import ast
import operator


def ls(current_dir, *args):
    # figure out if the path is absolute or not
    path = args[0].strip()
    if len(path) < 0:
        path = "."

    if path[0] == "/":
        directory = path
    
    else:
        directory = current_dir 

    directory = path if args else current_dir
    try:
        for entry in os.listdir(directory):
            print(entry)
    except Exception as e:
        print(f"ls: cannot access '{directory}': {e}")

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
