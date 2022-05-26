import sqlite3
import sys


def connect_database(db):
    """Connects to a specified sqlite database.

    Args:
        db: A path to a sqlite database file. String
    Returns:
        A sqlite3 database connection object.
    """
    con = None

    try:
        con = sqlite3.connect(db)
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
