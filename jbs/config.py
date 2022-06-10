# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)

def get_config(config_file: os.PathLike) -> dict:
    """Gets the contents of a specified JSON file

    Args:
        config_file: A path to a JSON config file 

    Returns:
        dictionary: a dictionary containing the key:value pairs from the 
        config file
    """
    with open(file=config_file, mode='r') as config_temp:
        config = json.load(config_temp)

    logger.info('Opened config file')
    logger.debug(config_file)

    return config


def get_update_version(update_version_file: os.PathLike) -> int:
    """gets the schema update version from a specified JSON file

    Args:
        update_version_file: A path to the schema update verion file.

    Returns:
        integer: an integer with the version of the most up to date schema
    """
    with open(file=update_version_file, mode='r') as version_temp:
        schema_version = json.load(version_temp)

    logger.info('Opened schema config file')
    logger.debug(update_version_file)

    return schema_version['version']
