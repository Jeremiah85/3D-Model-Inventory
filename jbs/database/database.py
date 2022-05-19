import sqlite3
import sys

def connect_database(db):
    con = None

    try:
        con = sqlite3.connect(db)
        return con

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def get_all_models(connection):

    try:
        cur = connection.cursor()
        
        cur.execute("SELECT Model_Name, Set_Name, Artist_Name, Source_Name "
                    "FROM tblModel AS m "
                    "INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID "
                    "INNER JOIN tblSource AS s ON m.Source = s.Source_ID;"
                    )

        return cur.fetchall()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)

def close_database(connection):

    try:
        if connection:
            connection.close()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)
