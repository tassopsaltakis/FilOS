import os
import shutil
from user_management import UserManagement

# Establish FilOS root directory as one level up from this script
FIL_OS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Possible user statuses
NORMAL_USER = 0
SUPER_USER = 1

# Current user status - defaulting to normal user
current_user_status = NORMAL_USER

# Session token for superuser
superuser_session_token = None

def su():
    global current_user_status
    global superuser_session_token
    user_mgmt = UserManagement()
    superuser_password = input("Enter superuser password: ")
    if user_mgmt.authenticate_superuser(superuser_password):
        print("Superuser mode activated.")
        current_user_status = SUPER_USER
        superuser_session_token = os.urandom(16)
    else:
        print("Superuser authentication failed.")

def ls(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            print(file)
    except Exception as e:
        print(f"ls: cannot access '{directory}': {e}")

def cd(current_dir, target_dir):
    new_path = os.path.normpath(os.path.join(current_dir, target_dir))
    if not new_path.startswith(FIL_OS_ROOT):
        print(f"cd: Access denied: you are at {current_dir}")
        return current_dir

    if os.path.isdir(new_path):
        return new_path
    else:
        print(f"cd: no such file or directory: {target_dir}")
        return current_dir

def pwd(current_dir):
    return current_dir

def mkdir(current_dir, dirname):
    new_path = os.path.join(current_dir, dirname)
    try:
        os.makedirs(new_path)
        print(f"Directory created at {new_path}")
    except Exception as e:
        print(f"mkdir: cannot create directory '{dirname}': {e}")

def rmdir(current_dir, dirname):
    dir_path = os.path.join(current_dir, dirname)
    try:
        os.rmdir(dir_path)
        print(f"Directory removed: {dir_path}")
    except Exception as e:
        print(f"rmdir: failed to remove '{dirname}': {e}")

def touch(current_dir, filename):
    file_path = os.path.join(current_dir, filename)
    try:
        open(file_path, 'a').close()
        os.utime(file_path, None)
    except Exception as e:
        print(f"touch: cannot touch '{filename}': {e}")

def cat(current_dir, filename):
    file_path = os.path.join(current_dir, filename)
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except Exception as e:
        print(f"cat: cannot open '{filename}': {e}")

def rm(filename):
    if current_user_status != SUPER_USER:
        print("Operation not permitted: requires superuser privileges.")
        return
    
    try:
        os.remove(filename)
        print(f"Removed {filename}")
    except Exception as e:
        print(f"rm: cannot remove '{filename}': {e}")

def cp(source, destination):
    try:
        shutil.copy(source, destination)
        print(f"Copied {source} to {destination}")
    except Exception as e:
        print(f"cp: cannot copy '{source}': {e}")

def mv(source, destination):
    try:
        shutil.move(source, destination)
        print(f"Moved {source} to {destination}")
    except Exception as e:
        print(f"mv: cannot move '{source}': {e}")

def echo(text):
    print(text)

if __name__ == "__main__":
    while True:
        command_line = input("$ ").strip()
        parts = command_line.split()
        command = parts[0]
        args = parts[1:]

        if command == 'su':
            su()
        elif command == 'ls':
            ls(FIL_OS_ROOT)
        elif command == 'cd':
            if args:
                FIL_OS_ROOT = cd(FIL_OS_ROOT, args[0])
        elif command == 'pwd':
            print(pwd(FIL_OS_ROOT))
        elif command == 'mkdir':
            if args:
                mkdir(FIL_OS_ROOT, args[0])
        elif command == 'rmdir':
            if args:
                rmdir(FIL_OS_ROOT, args[0])
        elif command == 'touch':
            if args:
                touch(FIL_OS_ROOT, args[0])
        elif command == 'cat':
            if args:
                cat(FIL_OS_ROOT, args[0])
        elif command == 'rm':
            if args:
                rm(args[0])
        elif command == 'cp':
            if len(args) >= 2:
                cp(args[0], args[1])
        elif command == 'mv':
            if len(args) >= 2:
                mv(args[0], args[1])
        elif command == 'echo':
            if args:
                echo(" ".join(args))
        elif command == 'exit':
            print("Exiting FilOS.")
            break
        else:
            print(f"Command '{command}' not recognized.")
