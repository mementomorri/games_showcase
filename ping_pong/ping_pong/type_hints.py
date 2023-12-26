from typing import NamedTuple


class SpriteCoordinates(NamedTuple):  # typehint for coordinates
    x: int
    y: int


class SpriteSize(NamedTuple):  # typehint for sprite sizes
    width: int
    height: int
