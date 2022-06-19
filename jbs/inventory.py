# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import dataclasses
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.NOTSET)


@dataclasses.dataclass
class Model:
    """A object representing a 3D model.

    Attributes:
        id: The id of the model.
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
    id: int
    model: str
    set: str
    artist: Any
    source: Any
    source_note: str
    supports: bool | int
    format: str
    folder: str
    printed: bool | int

    def astuple(self, exclude: Optional[str]=None) -> tuple:
        self.exclude = exclude
        if not self.exclude:
            return dataclasses.astuple(self)
        else:
            return tuple(getattr(self, field.name) for field in 
                dataclasses.fields(self) if field.name != self.exclude)


@dataclasses.dataclass
class Artist:
    """A object representing an artist.

    Attributes:
        id: The id of the artist.
        name: The artist's name.
        website: The artist's website.
        email: The artists's email.
        folder: What base folder the artist's models are in.
    """
    id: int
    name: str
    website: str
    email: str
    folder: str

    def astuple(self, exclude: Optional[str]=None) -> tuple:
        self.exclude = exclude
        if not self.exclude:
            return dataclasses.astuple(self)
        else:
            return tuple(getattr(self, field.name) for field in 
                dataclasses.fields(self) if field.name != self.exclude)


@dataclasses.dataclass
class Source:
    """A object representing a source.

    Attributes:
        id: The id of the source.
        name: The source's name.
        website: The source's website.
    """
    id: int
    name: str
    website: str

    def astuple(self, exclude: Optional[str]=None) -> tuple:
        self.exclude = exclude
        if not self.exclude:
            return dataclasses.astuple(self)
        else:
            return tuple(getattr(self, field.name) for field in 
                dataclasses.fields(self) if field.name != self.exclude)


class ObjectFactory:
    def __init__(self):
        pass

    def createModel(self, args: Any) -> Model:
        self._instance = Model(
            id = args[0],
            model = args[1],
            set = args[2],
            artist = args[3],
            source = args[4],
            source_note = args[5],
            supports = bool(args[6]),
            format = args[7],
            folder = args[8],
            printed = bool(args[9])
        )

        return self._instance

    def createArtist(self, args: Any) -> Artist:
        self._instance = Artist(
            id = args[0],
            name = args[1],
            website = args[2],
            email = args[3],
            folder = args[4]
        )

        return self._instance

    def createSource(self, args: Any) -> Source:
        self._instance = Source(
            id = args[0],
            name = args[1],
            website = args[2]
        )

        return self._instance
