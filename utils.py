import os
import json
import yaml
import clang.cindex


def extract_includes(c_file_path, src_folder_path):
    # Initialize Clang index
    index = clang.cindex.Index.create()
    # Parse the C file
    translation_unit = index.parse(c_file_path, args=['-x', 'c', '-std=c11'])
    file_paths = [x.include.name for x in translation_unit.get_includes()]
    final_names = [f"#include <{path.split('/')[-1]}>" 
                   if path.startswith('/usr/include') else path for path in file_paths]
    final_names = [f'#include "{path.split("/")[-1]}"'
                   if path.startswith(src_folder_path) else path for path in final_names]
    return "\n".join(final_names)

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
    config['harness'] =  f"harness_{config['function_name']}.{'c' if config['is_c_code'] else 'cpp'}"
    config['harness_bin'] =  f"harness_{config['function_name']}"
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