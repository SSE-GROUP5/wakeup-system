
import os

def read_env_file(env_file):
    if not os.path.exists(env_file):
        return {}
    already_env_vars = {}
    with open(env_file) as file:
        lines = file.readlines()
        for line in lines:
            key, value = line.strip().split("=")
            already_env_vars[key] = value
            
    return already_env_vars
 
def get_env_vars(env_file, key):
    if not os.path.exists(env_file):
        return None
    with open(env_file) as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith(key):
                return line.strip().split("=")[1]
    return None

