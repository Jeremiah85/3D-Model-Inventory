import json

def get_config(config_file):
    with open(config_file, 'r') as config_temp:
        config = json.load(config_temp)

    return config
