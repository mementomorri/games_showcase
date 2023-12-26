from typing import NamedTuple


degrees = int


class Position(NamedTuple):
    x: int
    y: int
    z: int | None


class RGBA(NamedTuple):
    red: int | float
    green: int | float
    blue: int | float
    alpha: int | float


class IMapmanager:
    def _get_color(self) -> RGBA:
        pass

    def _find_blocks(self, pos):
        pass

    def _clear(self) -> None:
        pass

    def add_block(self, position: Position) -> None:
        pass

    def load_land(self, filename) -> Position:
        pass

    def is_empty(self, pos: Position) -> bool:
        pass

    def find_highest_empty(self, pos: Position) -> Position:
        pass

    def build_block(self, pos: Position) -> None:
        pass

    def del_block(self, position: Position) -> None:
        pass

    def del_block_from(self, position: Position) -> None:
        pass

    def save_map(self) -> None:
        pass

    def load_map(self) -> None:
        pass


