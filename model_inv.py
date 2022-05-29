# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os
import sys

import jbs.config as config
import jbs.database.database_utils as db
import jbs.gui as gui

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep
default_database = scriptpath + "3D_Models.db"
sql_schema_new = scriptpath + 'sql' + os.sep +'empty_database.sql'
sql_schema_update = scriptpath + 'sql' + os.sep +'update_database.sql'
sql_update_version = scriptpath + 'sql' + os.sep +'schema_version.json'
default_config = scriptpath + "config.json"

def main():
    # Determine how to connect to the database. Either default location, 
    # location specified in the config file, or create a new database
    if os.path.exists(default_database):
        connection = db.connect_database(default_database)
    elif os.path.exists(default_config):
        configuration = config.get_config(default_config)
        connection = db.connect_database(configuration['database'])
    else:
        connection = db.connect_database(default_database)
        db.modify_database_schema(connection, sql_schema_new)

# Check if a database update is needed
    file_version = config.get_update_version(sql_update_version)
    db_version = db.check_database_schema(connection)

    if file_version > db_version:
        db.modify_database_schema(connection, sql_schema_update)
    else:
        pass

    app = gui.Window(connection)
    app.root.mainloop()

    db.close_database(connection)

if __name__ == '__main__':
    main()
