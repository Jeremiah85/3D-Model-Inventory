# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import dataclasses
import logging
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


@dataclasses.dataclass
class Model:
    """A object representing a 3D model.

    Attributes:
        model: The model's name.
        set: The model's set.
        artist: The model's artist.
        source: The model's source.
        source_note: And note about the model's source.
        supports: Whether the model is supported.
        format: What formats the model is in.
        folder: What base folder the model is in.
        printed: Whether the model has been printed.
    """
    model: str
    set: str
    artist: Any
    source: Any
    source_note: str
    supports: bool | int
    format: str
    folder: str
    printed: bool | int

    def astuple(self) -> tuple:
        return dataclasses.astuple(self)


@dataclasses.dataclass
class Artist:
    """A object representing an artist.

    Attributes:
        name: The artist's name.
        website: The artist's website.
        email: The artists's email.
        folder: What base folder the artist's models are in.
    """
    name: str
    website: str
    email: str
    folder: str

    def astuple(self) -> tuple:
        return dataclasses.astuple(self)


@dataclasses.dataclass
class Source:
    """A object representing a source.

    Attributes:
        name: The source's name.
        website: The source's website.
    """
    name: str
    website: str

    def astuple(self) -> tuple:
        return dataclasses.astuple(self)


class ObjectFactory:
    def __init__(self):
        pass

    def createModel(self, args: Any) -> Model:
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

    def createArtist(self, args: Any) -> Artist:
        self._instance = Artist(
            name = args[0],
            website = args[1],
            email = args[2],
            folder = args[3]
        )

        return self._instance

    def createSource(self, args: Any) -> Source:
        self._instance = Source(
            name = args[0],
            website = args[1]
        )

        return self._instance
