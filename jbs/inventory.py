# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


class Model:
    """A object representing a 3D model.

    Attributes:
        model: The model's name. String
        set: The model's set. String
        artist: The model's artist. String
        source: The model's source. String
        source_note: And note about the model's source. String
        supports: Whether the model is supported. Boolean
        format: What formats the model is in. String
        folder: What base folder the model is in. String 
        printed: Whether the model has been printed. Boolean
    """
    def __init__(self, args):
        """Takes a list of values and creates the object"""
        self.model = args[0]
        self.set = args[1]
        self.artist = args[2]
        self.source = args[3]
        self.source_note = args[4]
        self.supports = bool(args[5])
        self.format = args[6]
        self.folder = args[7]
        self.printed = bool(args[8])

    def to_list(self):
        """Creates a list from the object's values.

        Returns:
            Returns a list of the objects attribute values.
        """
        result = []
        result.append(self.model)
        result.append(self.set)
        result.append(self.artist)
        result.append(self.source)
        result.append(self.source_note)
        result.append(self.supports)
        result.append(self.format)
        result.append(self.folder)
        result.append(self.printed)

        return result


class Artist:
    """A object representing an artist.

    Attributes:
        name: The artist's name. String
        website: The artist's website. String
        email: The artists's email. String
        folder: What base folder the artist's models are in. String 
    """
    def __init__(self, args):
        """Takes a list of values and creates the object"""
        self.name = args[0]
        self.website = args[1]
        self.email = args[2]
        self.folder = args[3]

    def to_list(self):
        """Creates a list from the object's values.

        Returns:
            Returns a list of the objects attribute values.
        """
        result = []
        result.append(self.name)
        result.append(self.website)
        result.append(self.email)
        result.append(self.folder)

        return result


class Source:
    """A object representing a source.

    Attributes:
        name: The source's name. String
        website: The source's website. String
    """
    def __init__(self, args):
        """Takes a list of values and creates the object"""
        self.name = args[0]
        self.website = args[1]

    def to_list(self):
        """Creates a list from the object's values.

        Returns:
            Returns a list of the objects attribute values.
        """
        result = []
        result.append(self.name)
        result.append(self.website)

        return result
