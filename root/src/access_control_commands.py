import os

script_dir = os.path.dirname(os.path.realpath('__file__'))
root_dir = os.path.abspath(os.path.join(script_dir, '..', '..', 'root'))
config_dir = os.path.join(root_dir, 'config')
access_index_commands = os.path.join(config_dir, 'access_index_commands.txt')


def load_access_data():
    """
    Loads and categorizes access rules from the access index file.

    Parameters:
    - access_index_path: The path to the access index file.

    Returns:
    A dictionary with categorized access data for directories and commands.
    """
    access_data = {'directories': {}, 'commands': {}}
    current_category = None

    with open(access_index_commands, 'r') as file:
        for line in file:
            line = line.strip()
            if line == ':directories:' or line == ':commands:':
                current_category = line[1:-1]  # Remove colons
            elif current_category and line:
                resource, groups = line.split(':', 1)
                access_data[current_category][resource] = groups.split(',')

    return access_data

def load_user_groups(groups_file, user_name):
    """
    Loads the groups that a specific user belongs to.

    Parameters:
    - groups_file: The path to the file containing group memberships.
    - user_name: The name of the user.

    Returns:
    A list of groups the user belongs to.
    """
    user_groups = []

    with open(groups_file, 'r') as file:
        for line in file:
            group_name, members = line.strip().split(':', 1)
            if user_name in members.split(','):
                user_groups.append(group_name)

    return user_groups

def check_user_access(user_name, resource, resource_type, groups_file, root_dir):
    """
    Checks if a user has access to a specified resource (directory or command) based on group memberships.

    Parameters:
    - user_name: The name of the user whose access is being checked.
    - resource: The resource (directory or command) to check access for.
    - resource_type: The type of the resource ('directory' or 'command').
    - access_index_path: The path to the access index file.
    - groups_file: The path to the file containing group memberships.
    - root_dir: The FilOS root directory path (used for directory resources).

    Returns:
    True if the user has access, False otherwise.
    """
    access_data = load_access_data(access_index_commands)
    user_groups = load_user_groups(groups_file, user_name)

    # Adjust resource path for directory type
    if resource_type == 'directory':
        resource = os.path.join(root_dir, resource)  # Construct the path relative to root_dir

    allowed_groups = access_data[resource_type + 's'].get(resource, [])

    # Check if any of the user's groups are in the allowed groups for the resource
    return any(group in user_groups for group in allowed_groups)

def update_access_index_for_new_user(new_user_directory, new_user_name):
    """
    Updates the access_index_commands.txt file to grant default access rights for a new user and superuser.

    Parameters:
    - access_index_path: The path to the access index file.
    - new_user_directory: The directory created for the new user.
    - new_user_name: The username of the newly created user.
    """
    # Read the current access data
    with open(access_index_commands, 'r') as file:
        lines = file.readlines()

    # Assume superuser group is named "superuser"; adjust as needed
    superuser_group = "superuser"
    user_group = new_user_name  # Assuming user's group is the same as their username; adjust as needed

    # Prepare the new entries for the access index
    new_user_access = f"{new_user_directory}:{new_user_name}\n"
    superuser_access = f"{new_user_directory}:{superuser_group}\n"

    # Append new entries if they don't already exist
    if new_user_access not in lines:
        lines.append(new_user_access)
    if superuser_access not in lines:
        lines.append(superuser_access)

    # Write the updated access data back to the file
    with open(access_index_commands, 'w') as file:
        file.writelines(lines)
