# commands.py
import os

def ls(directory):
    try:
        files = os.listdir(directory)
        for file in files:
            print(file)
    except Exception as e:
        print(f"ls: cannot access '{directory}': {e}")

def cd(current_dir, target_dir):
    new_path = os.path.join(current_dir, target_dir)
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
        with open(file_path, 'a'):
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

# Implement additional functions for rm, cp, mv, echo, etc.
