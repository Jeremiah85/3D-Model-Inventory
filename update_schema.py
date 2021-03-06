# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys

import jbs.config as config
import jbs.database.database_utils as db

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
default_database = scriptpath + "3D_Models.db"
sql_update = scriptpath + 'sql' + os.sep +'update_database.sql'
default_config = scriptpath + "config.json"

def main():
    if os.path.exists(default_database):
        connection = db.connect_database(default_database)
        db.modify_database_schema(connection, sql_update)
        db.close_database(connection)
    elif os.path.exists(default_config):
        configuration = config.get_config(default_config)
        connection = db.connect_database(configuration['database'])
        db.modify_database_schema(connection, sql_update)
        db.close_database(connection)
    else:
        print("No Database Found")

if __name__ == '__main__':
    main()
