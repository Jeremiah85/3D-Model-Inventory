# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import sqlite3
import sys


def check_database_schema(connection):
    """Gets the database schema of the current database

    Args:
        connection: A sqlite3 database connection

    Returns:
        integer: the current database schema version
    """
    try:
        cur = sqlite3.Cursor(connection)
        cur.execute('SELECT version '
            'FROM tblSchema '
            'WHERE label = "current";'
            )
        
        result = cur.fetchone()
        return result[0]

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def modify_database_schema(connection, sql_file):
    """Takes a sql file and runs it against a database.

    This method updates a database with the contents of a sql file.
    Args:
        connection: A sqlite3 database connection
        sql_file: a file path to a sql file containing sql commands
    """
    cur = sqlite3.Cursor(connection)
    with open(file=sql_file, mode='r') as sql:
        sql_query = sql.read()

    try:
        cur.executescript(sql_query)
        connection.commit()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def connect_database(database):
    """Connects to a specified sqlite database.

    Args:
        db: A path to a sqlite database file. String
    Returns:
        A sqlite3 database connection object.
    """
    con = None

    try:
        con = sqlite3.connect(database)
        return con

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def close_database(connection):
    """Closes the database connection.

    Args:
        connection: The database connection to close.
    """
    try:
        if connection:
            connection.close()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)
