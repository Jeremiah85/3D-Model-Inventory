# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json


def get_config(config_file):
    """Gets the contents of a specified JSON file

    Args:
        config_file: A string containing a path to a JSON config file 

    Returns:
        dictionary: a dictionary containing the key:value pairs from the 
        config file
    """
    with open(config_file, 'r') as config_temp:
        config = json.load(config_temp)

    return config


def get_update_version(update_version_file):
    """gets the schema update version from a specified JSON file

    Args:
        update_version_file: A string containing a path to the schema update
        verion file.

    Returns:
        integer: an integer with the version of the most up to date schema
    """
    with open(update_version_file, 'r') as version_temp:
        schema_version = json.load(version_temp)

    return schema_version['version']
