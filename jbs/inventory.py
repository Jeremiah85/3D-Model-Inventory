# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import dataclasses
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


@dataclasses.dataclass
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
    model: str
    set: str
    artist: str
    source: str
    source_note: str
    supports: bool
    format: str
    folder: str
    printed: str

    def astuple(self):
        return dataclasses.astuple(self)


@dataclasses.dataclass
class Artist:
    """A object representing an artist.

    Attributes:
        name: The artist's name. String
        website: The artist's website. String
        email: The artists's email. String
        folder: What base folder the artist's models are in. String 
    """
    name: str
    website: str
    email: str
    folder: str

    def astuple(self):
        return dataclasses.astuple(self)


@dataclasses.dataclass
class Source:
    """A object representing a source.

    Attributes:
        name: The source's name. String
        website: The source's website. String
    """
    name: str
    website: str

    def astuple(self):
        return dataclasses.astuple(self)


class ObjectFactory:
    def __init__(self):
        pass

    def createModel(self, args):
        self._instance = Model(
            model = args[0],
            set = args[1],
            artist = args[2],
            source = args[3],
            source_note = args[4],
            supports = bool(args[5]),
            format = args[6],
            folder = args[7],
            printed = bool(args[8])
        )

        return self._instance

    def createArtist(self, args):
        self._instance = Artist(
            name = args[0],
            website = args[1],
            email = args[2],
            folder = args[3]
        )

        return self._instance

    def createSource(self, args):
        self._instance = Source(
            name = args[0],
            website = args[1]
        )

        return self._instance
