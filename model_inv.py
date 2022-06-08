# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import os
import sys

# jbs.logging is imported to create the root logger before the other modules
# are imported otherwise they get a different root logger.
import jbs.logging
import jbs.config as config
import jbs.database.database_utils as db
import jbs.gui as gui

scriptpath = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep

default_database = f'{scriptpath}3D_Models.db'
sql_schema_new = f'{scriptpath}sql{os.sep}empty_database.sql'
sql_schema_update = f'{scriptpath}sql{os.sep}update_database.sql'
sql_update_version = f'{scriptpath}sql{os.sep}schema_version.json'
default_config = f'{scriptpath}config.json'


def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.NOTSET)

    logger.info("Starting Application")
    # Determine how to connect to the database. Either default location, 
    # location specified in the config file, or create a new database
    if os.path.exists(path=default_database):
        logger.info("Using default database")
        logger.debug(default_database)
        connection = db.connect_database(database=default_database)
    elif os.path.exists(path=default_config):
        logger.info("Using database from config file")
        configuration = config.get_config(config_file=default_config)
        logger.debug(configuration['database'])
        connection = db.connect_database(database=configuration['database'])
    else:
        logger.info("No database, Creating New")
        connection = db.connect_database(database=default_database)
        logger.debug(default_database)
        db.modify_database_schema(
            connection=connection,
            sql_file=sql_schema_new
            )
        logger.info("Database has been created")

    # Check if a database update is needed
    file_version = config.get_update_version(
        update_version_file=sql_update_version
        )
    logger.debug(f"Newest schema is {file_version}")
    db_version = db.check_database_schema(connection=connection)
    logger.debug(f"Database schema is {db_version}")

    if file_version > db_version:
        logger.debug("Schema update is needed")
        db.modify_database_schema(
            connection=connection,
            sql_file=sql_schema_update
            )
        logger.info("Schema update has been applied")
    else:
        pass

    app = gui.Window(connection)
    app.root.mainloop()

    logger.info("closing the database connection")
    db.close_database(connection=connection)

if __name__ == '__main__':
    main()
