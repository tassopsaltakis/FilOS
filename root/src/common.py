import os
current_user_info = {'username': None, 'is_superuser': False}

username = current_user_info.get('username')

"""system directories"""
script_dir = os.path.dirname(os.path.realpath('__file__'))
root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))
config_dir = os.path.join(root_dir, 'config')
home_dir = os.path.join(root_dir, 'home')

"""system files"""
users_file = os.path.join(config_dir, 'users.txt')
groups_file = os.path.join(config_dir, 'groups.txt')
commands_file = os.path.join(config_dir, 'commands.txt')
access_index_commands = os.path.join(config_dir, 'access_index_commands.txt')
access_index_dirs = os.path.join(config_dir, 'access_index_dirs.txt')