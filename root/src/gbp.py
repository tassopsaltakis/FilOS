import os
from common import groups_file, access_index_dirs, home_dir

def load_groups():
    """Load group memberships from the predefined groups file."""
    groups = {}
    with open(groups_file, 'r') as file:
        for line in file:
            group_name, members = line.strip().split(':')
            groups[group_name] = members.split(',')
    return groups

def check_directory_access(username, directory):
    """Check if the user has access to a specified directory."""
    groups = load_groups()
    user_groups = [group for group, members in groups.items() if username in members]

    user_home_dir = os.path.normcase(os.path.join(home_dir, username))
    abs_directory = os.path.normcase(os.path.abspath(directory))

    # Superusers have universal access
    if 'superuser' in user_groups:
        return True

    # Check if the directory is within the user's home directory
    if abs_directory.startswith(user_home_dir):
        return True

    # Load directory access rules for additional directories outside home
    with open(access_index_dirs, 'r') as file:
        for line in file:
            dir_path, allowed_groups = line.strip().split(':')
            dir_path = os.path.normcase(os.path.abspath(dir_path))
            if abs_directory.startswith(dir_path):
                return any(group in user_groups for group in allowed_groups.split(','))

    # Default deny if not explicitly allowed
    return False