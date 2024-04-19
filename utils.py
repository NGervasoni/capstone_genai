import os
import json
import yaml


def load_config(config_file):
    """
    Load configuration values from a YAML file.
    
    Args:
        config_file (str): The file path of the YAML configuration file.
    
    Returns:
        dict: A dictionary containing configuration values.
    """
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config
    


def find_files(directory, extension):
    """
    Search for files with a specific extension within a given directory, including subdirectories.

    Args:
    directory (str): The path to the directory to search.
    extension (str): The file extension to search for.

    Returns:
    list: A list of paths to files that match the given extension.
    """
    matched_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                matched_files.append(os.path.join(root, file))
    return matched_files