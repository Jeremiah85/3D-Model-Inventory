# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json

def get_config(config_file):
    with open(config_file, 'r') as config_temp:
        config = json.load(config_temp)

    return config
