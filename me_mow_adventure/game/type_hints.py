from typing import NamedTuple


class Coordinate(NamedTuple):  # typehint для координат
    x: int
    y: int


class Speed(NamedTuple):  # typehint для скорости перемещения объектов
    x: int
    y: int

