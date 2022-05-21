import sqlite3
import sys
import jbs.model.model as mdl

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
        cur.execute("SELECT Model_Name, Set_Name, Artist_Name, Source_Name, "
                    "Source_Note, Supports, Format, Artist_Folder, Printed "
                    "FROM tblModel AS m "
                    "INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID "
                    "INNER JOIN tblSource AS s ON m.Source = s.Source_ID;"
                    )
        results = cur.fetchall()

        models = []
        for model in results:
            models.append(mdl.Model(model))

        return models
        
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

def get_all_artists(connection):

    try:
        cur = connection.cursor()
        cur.execute("SELECT Artist_Name, Artist_Website, Artist_Email, Artist_Folder "
                    "FROM tblArtist;"
                    )
        results = cur.fetchall()

        artists = []
        for artist in results:
            artists.append(mdl.Artist(artist))

        return artists
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)

def get_all_sources(connection):

    try:
        cur = connection.cursor()
        cur.execute("SELECT Source_Name, Source_Website "
                    "FROM tblSource;"
                    )
        results = cur.fetchall()

        sources = []
        for source in results:
            sources.append(mdl.Source(source))

        return sources
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)

# TODO: Add Model search
# TODO: Add Artist search
# TODO: Add Source search

# TODO: Add New Model
# TODO: Add New Artist
# TODO: Add New Source

def close_database(connection):

    try:
        if connection:
            connection.close()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)
