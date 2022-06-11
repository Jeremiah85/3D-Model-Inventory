# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
import sqlite3
import sys

import jbs.inventory as inv

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


def get_all_models(connection: sqlite3.Connection) -> list[inv.Model] | inv.Model:
    """Returns a list of all model objects from the database.

    Queries the database and retrieves all of the models then converts
    that list to a list of model objects.

    Args:
        connection: A sqlite database connection.

    Returns:
        A list of all model objects in the database.
    """
    factory = inv.ObjectFactory()
    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Model_Name, Set_Name, Artist_Name, Source_Name, '
                'Source_Note, Supports, Format, Artist_Folder, Printed '
            'FROM tblModel AS m '
            'INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID '
            'INNER JOIN tblSource AS s ON m.Source = s.Source_ID;'
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} models")

        if results:
            models = []
            for model in results:
                models.append(factory.createModel(model))
        else:
            models = results

        return models
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def get_all_artists(connection: sqlite3.Connection) -> list[inv.Artist] | inv.Artist:
    """Returns a list of all artist objects from the database.

    Queries the database and retrieves the artists then converts
    that list to a list of artist objects.

    Args:
        connection: A sqlite database connection.

    Returns:
        A list of all artist objects in the database.
    """
    factory = inv.ObjectFactory()
    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Artist_Name, Artist_Website, Artist_Email, Artist_Folder '
            'FROM tblArtist;'
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} artists")

        if results:
            artists = []
            for artist in results:
                artists.append(factory.createArtist(artist))
        else:
            artists = results

        return artists
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def get_all_sources(connection: sqlite3.Connection) -> list[inv.Source] | inv.Source:
    """Returns a list of all source objects from the database.

    Queries the database and retrieves the sources then converts
    that list to a list of source objects.

    Args:
        connection: A sqlite database connection.

    Returns:
        A list of all source objects in the database.
    """
    factory = inv.ObjectFactory()
    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Source_Name, Source_Website '
            'FROM tblSource;'
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} sources")

        if results:
            sources = []
            for source in results:
                sources.append(factory.createSource(source))
        else:
            sources = results

        return sources
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def search_model(
    connection: sqlite3.Connection,
    field: str,
    search_text: str
    ) -> list[inv.Model] | inv.Model:
    """Retrieves all model objects matching a user query.

    Connects to the database and searches a user supplied field for
    a user supplied string and returns a list of matching items as 
    a list of model objects.

    Args:
        connection: A sqlite database connection.
        field: The field in the model table to search.
        search_text: the text to search for.

    Returns:
        A list of model objects matching the user's query.
    """
    factory = inv.ObjectFactory()
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Model_Name, Set_Name, Artist_Name, Source_Name, '
                'Source_Note, Supports, Format, Artist_Folder, Printed '
            'FROM tblModel AS m '
            'INNER JOIN tblArtist AS a ON m.Artist = a.Artist_ID '
            'INNER JOIN tblSource AS s ON m.Source = s.Source_ID '
            f'WHERE m.{field} LIKE :keyword;', search_term
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} models")

        if results:
            models = []
            for model in results:
                models.append(factory.createModel(model))
        else:
            models = results

        return models
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def search_artist(
    connection: sqlite3.Connection,
    search_text: str
    ) -> list[inv.Artist] | inv.Artist:
    """Retrieves all artist objects matching a user query.

    Connects to the database and searches for a user supplied string
    and returns a list of matching items as a list of artist objects.

    Args:
        connection: A sqlite database connection.
        search_text: the text to search for.

    Returns:
        A list of artist objects matching the user's query.
    """
    factory = inv.ObjectFactory()
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Artist_Name, Artist_Website, Artist_Email, Artist_Folder '
            'FROM tblArtist '
            'WHERE Artist_Name LIKE :keyword '
            'OR Artist_Website LIKE :keyword '
            'OR Artist_Email LIKE :keyword;', search_term
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} artists")

        if results:
            artists = []
            for artist in results:
                artists.append(factory.createArtist(artist))
        else:
            artists = results

        return artists
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def search_source(
    connection: sqlite3.Connection,
    search_text: str
    ) -> list[inv.Source] | inv.Source:
    """Retrieves all source objects matching a user query.

    Connects to the database and searches for a user supplied
    string and returns a list of matching items as a list of
    source objects.

    Args:
        connection: A sqlite database connection.
        search_text: the text to search for.

    Returns:
        A list of source objects matching the user's query.
    """
    factory = inv.ObjectFactory()
    search_term = {'keyword': '%' + search_text + '%'}

    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Source_Name, Source_Website '
            'FROM tblSource '
            'WHERE Source_Name LIKE :keyword OR Source_Website LIKE :keyword;',
            search_term
            )
        results = cur.fetchall()

        logger.debug(f"Query returned {len(results)} sources")

        if results:
            sources = []
            for source in results:
                sources.append(factory.createSource(source))
        else:
            sources = results

        return sources
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def add_model(connection: sqlite3.Connection, model: inv.Model) -> None:
    """Adds a supplied model object to the database

    Takes a model object and extracts the attributes to insert them
    into the database.

    Args:
        connection: A sqlite database connection.
        model: A model object to add to the database.
    """
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

    logger.info("Resolving artist name to artist ID")
    artist_id = get_artist_id(connection=connection, artist_name=model.artist)
    logger.info("Resolving source name to source ID")
    source_id = get_source_id(connection=connection, source_name=model.source)

    model.artist = artist_id
    model.source = source_id

    try:
        cur = connection.cursor()
        logger.info("Adding model to the database")
        cur.execute(
            'INSERT INTO tblModel ('
                'Model_Name, '
                'Artist, '
                'Set_Name, '
                'Source, '
                'Source_Note, '
                'Supports, '
                'Format, '
                'Printed) '
            'VALUES ('
                ':model, '
                ':artist, '
                ':set, '
                ':source, '
                ':source_note, '
                ':supports, '
                ':format, '
                ':printed);', 
            vars(model)
            )
        connection.commit()
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def add_artist(connection: sqlite3.Connection, artist: inv.Artist) -> None:
    """Adds a supplied artist object to the database

    Takes a artist object and extracts the attributes to insert them
    into the database.

    Args:
        connection: A sqlite database connection.
        artist: A artist object to add to the database.
    """
    try:
        cur = connection.cursor()
        logger.info("Adding artist to the database")
        cur.execute(
            'INSERT INTO tblArtist ('
                'Artist_Name, '
                'Artist_Website, '
                'Artist_Email, '
                'Artist_Folder) '
                'VALUES ('
                ':name, '
                ':website, '
                ':email, '
                ':folder);', 
            vars(artist)
            )
        connection.commit()
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def add_source(connection: sqlite3.Connection, source: inv.Source) -> None:
    """Adds a supplied source object to the database

    Takes a source object and extracts the attributes to insert them
    into the database.

    Args:
        connection: A sqlite database connection.
        source: A source object to add to the database.
    """
    try:
        cur = connection.cursor()
        logger.info("Adding source to the database")
        cur.execute(
            'INSERT INTO tblSource (Source_Name, Source_Website) '
            'VALUES (:name, :website);', vars(source)
            )
        connection.commit()
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def get_artist_id(connection: sqlite3.Connection, artist_name: str) -> int:
    """Gets the ID for a supplied artist name.

    Takes a artist name and gets its ID from the database.

    Args:
        connection: A sqlite database connection.
        artist_name: The artist's name to look up.

    Returns:
        An integer containing the artist ID for the supplied artist.
    """
    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Artist_ID '
            'FROM tblArtist '
            'WHERE Artist_Name = :artist;', {'artist': artist_name}
            )
        results = cur.fetchone()

        logger.debug(f"{artist_name} equals {results[0]}")
        return results[0]
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)


def get_source_id(connection: sqlite3.Connection, source_name: str) -> int:
    """Gets the ID for a supplied source name.

    Takes a source name and gets its ID from the database.

    Args:
        connection: A sqlite database connection.
        source_name: The artist's name to look up.

    Returns:
        An integer containing the source ID for the supplied source.
    """
    try:
        cur = connection.cursor()
        cur.execute(
            'SELECT Source_ID '
            'FROM tblSource '
            'WHERE Source_Name = :source;', {'source': source_name}
            )
        results = cur.fetchone()

        logger.debug(f"{source_name} equals {results[0]}")
        return results[0]
    except sqlite3.Error as e:
        logger.error(e)
        sys.exit(1)
