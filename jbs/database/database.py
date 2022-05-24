import sqlite3
import sys
import jbs.model.model as mdl
# TODO: consider splitting this file into database utilities and queries


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
        cur.execute('SELECT Model_Name, Set_Name, Artist_Name, Source_Name, '
                        'Source_Note, Supports, Format, Artist_Folder, Printed '
                    'FROM tblModel AS m '
                    'INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID '
                    'INNER JOIN tblSource AS s ON m.Source = s.Source_ID;')
        results = cur.fetchall()

        models = []
        for model in results:
            models.append(mdl.Model(model))

        return models
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def get_all_artists(connection):
    try:
        cur = connection.cursor()
        cur.execute('SELECT Artist_Name, Artist_Website, Artist_Email, Artist_Folder '
                    'FROM tblArtist;')
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
        cur.execute('SELECT Source_Name, Source_Website '
                    'FROM tblSource;')
        results = cur.fetchall()

        sources = []
        for source in results:
            sources.append(mdl.Source(source))

        return sources
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def search_model(connection, field, search_text):
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute('SELECT Model_Name, Set_Name, Artist_Name, Source_Name, '
                        'Source_Note, Supports, Format, Artist_Folder, Printed '
                    'FROM tblModel AS m '
                    'INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID '
                    'INNER JOIN tblSource AS s ON m.Source = s.Source_ID '
                    f'WHERE m.{field} LIKE :keyword;', search_term)
        results = cur.fetchall()

        models = []
        for model in results:
            models.append(mdl.Model(model))

        return models
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def search_artist(connection, search_text):
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute('SELECT Artist_Name, Artist_Website, Artist_Email, Artist_Folder '
                    'FROM tblArtist '
                    'WHERE Artist_Name LIKE :keyword '
                    'OR Artist_Website LIKE :keyword '
                    'OR Artist_Email LIKE :keyword;', search_term)
        results = cur.fetchall()

        sources = []
        for source in results:
            sources.append(mdl.Source(source))

        return sources
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def search_source(connection, search_text):
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute('SELECT Source_Name, Source_Website '
                    'FROM tblSource '
                    'WHERE Source_Name LIKE :keyword OR Source_Website LIKE :keyword;', search_term)
        results = cur.fetchall()

        sources = []
        for source in results:
            sources.append(mdl.Source(source))

        return sources
        
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def add_model(connection, model):
    supports = model.supports
    match supports:
        case True:
            model.supports = 1
        case False:
            model.supports = 0
        case _:
            model.supports = 0

    printed = model.printed
    match printed:
        case True:
            model.printed = 1
        case False:
            model.printed = 0
        case _:
            model.printed = 0

    artist_id = get_artist_id(connection, model.artist)
    source_id = get_source_id(connection, model.source)

    model.artist = artist_id
    model.source = source_id

    try:
        cur = connection.cursor()
        cur.execute('INSERT INTO tblModel '
                    '(Model_Name, Artist, Set_Name, Source, Source_Note, Supports, Format, Printed) '
                    'VALUES '
                        '(:model, :set, :artist, :source, :source_note, :supports, :format, :printed);', vars(model))
        connection.commit()

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def add_artist(connection, artist):
    try:
        cur = connection.cursor()
        cur.execute('INSERT INTO tblArtist (Artist_Name, Artist_Website, Artist_Email, Artist_Folder) '
                    'VALUES (:name, :website, :email, :folder);', vars(artist))
        connection.commit()
    
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def add_source(connection, source):
    try:
        cur = connection.cursor()
        cur.execute('INSERT INTO tblSource (Source_Name, Source_Website) '
                    'VALUES (:name, :website);', vars(source))
        connection.commit()
    
    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def get_artist_id(connection, artist_id):
    try:
        cur = connection.cursor()
        cur.execute('SELECT Artist_ID '
                    'FROM tblArtist '
                    'WHERE Artist_Name = :artist;', {'artist': artist_id})
        results = cur.fetchone()

        return results[0]

    except sqlite3.Error as e:
        print(f"Error {e.args[0]}")
        sys.exit(1)


def get_source_id(connection, source_id):
    try:
        cur = connection.cursor()
        cur.execute('SELECT Source_ID '
                    'FROM tblSource '
                    'WHERE Source_Name = :source;', {'source': source_id})
        results = cur.fetchone()

        return results[0]

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
