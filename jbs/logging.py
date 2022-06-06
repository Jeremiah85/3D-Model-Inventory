import json
import logging
import logging.config
import os
import sys

def get_config(config_file):
    """Gets the contents of a specified JSON file

    Args:
        config_file: A string containing a path to a JSON config file 

    Returns:
        dictionary: a dictionary containing the key:value pairs from the 
        config file
    """
    with open(file=config_file, mode='r') as config_temp:
        config = json.load(config_temp)

    return config

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep

default_logfile_config = f'{scriptpath}logs{os.sep}run.log'
log_config = f'{scriptpath}logging.json'

logging_config = get_config(log_config)
if logging_config['handlers']['default']['filename'] == 'get_from_variable':
    logging_config['handlers']['default']['filename'] = default_logfile_config
logging.config.dictConfig(logging_config)
