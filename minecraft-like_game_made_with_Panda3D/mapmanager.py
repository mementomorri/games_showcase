import pickle
import sys

from conf import PATH_BASE_BLOCK, PATH_BASE_TEXTURE, PATH_MAP, BLOCK_COLORS
from type_hints import Position, IMapmanager, RGBA
from random import choice
from pathlib import Path


class Mapmanager(IMapmanager):
    """ Управление картой """
    def __init__(self) -> None:
        self.model = PATH_BASE_BLOCK  # модель кубика
        # текстура блока
        self.texture = PATH_BASE_TEXTURE
        self.colors = BLOCK_COLORS  # цвет в формате RGBA
        # создаём основу для новой карты
        self.land = render.attachNewNode("Land")  # узел, к которому привязаны все блоки карты

    def _get_color(self) -> RGBA: return RGBA(*choice(self.colors))

    def _find_blocks(self, position: Position): return self.land.findAllMatches("=at=" + str(position))

    def _clear(self) -> None:
        """обнуляет карту"""
        self.land.removeNode()
        self.land = render.attachNewNode("Land")

    def add_block(self, position: Position) -> None:
        # создаём строительные блоки
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(position)
        color = self._get_color()
        block.setColor(color)
        block.setTag("at", str(position))
        block.reparentTo(self.land)

    def load_land(self, land_file: Path) -> Position:
        """создаёт карту земли из текстового файла, возвращает её размеры"""
        self._clear()
        try:
            with open(land_file) as file:
                y = 0
                for line in file:
                    x = 0
                    line = line.split(' ')
                    for z in line:
                        for z0 in range(int(z) + 1):
                            self.add_block(Position(x, y, z0))
                        x += 1
                    y += 1
        except IOError as err:
            print(f"Could not open/read file: {land_file}. {err}")
            sys.exit()
        except Exception as err:
            print("Unexpected error:", err)
            sys.exit()

        return Position(x, y, None)

    def is_empty(self, position: Position) -> bool: return False if self._find_blocks(position) else True

    def find_highest_empty(self, position: Position) -> Position:
        x, y, z = position
        z = 1
        while not self.is_empty(Position(x, y, z)):
            z += 1
        return Position(x, y, z)

    def build_block(self, position: Position) -> None:
        """Ставим блок с учётом гравитации: """
        x, y, z = position
        new = self.find_highest_empty(position)
        if new[2] <= z + 1:
            self.add_block(new)

    def del_block(self, position: Position) -> None:
        """удаляет блоки в указанной позиции """
        blocks = self._find_blocks(position)
        for block in blocks:
            block.removeNode()

    def del_block_from(self, position: Position) -> None:
        x, y, z = self.find_highest_empty(position)
        pos = Position(x, y, z - 1)
        for block in self._find_blocks(pos):
            block.removeNode()

    def save_map(self) -> None:
        """сохраняет все блоки, включая постройки, в бинарный файл"""

        # возвращает коллекцию NodePath для всех существующих в карте мира блоков
        blocks = self.land.getChildren()
        # открываем бинарный файл на запись
        try:
            with open(PATH_MAP, 'wb') as fout:
                # сохраняем в начало файла количество блоков
                pickle.dump(len(blocks), fout)

                # обходим все блоки
                for block in blocks:
                    # сохраняем позицию
                    x, y, z = block.getPos()
                    pos = (int(x), int(y), int(z))
                    pickle.dump(pos, fout)
        except IOError as err:
            print(f"Can't open map file, there might be no such a file: {PATH_MAP}. {err}")
            sys.exit()
        except Exception as err:
            print("Unexpected error:", err)
            sys.exit()

    def load_map(self) -> None:
        # удаляем все блоки
        self._clear()

        try:
            # открываем бинарный файл на чтение
            with open(PATH_MAP, 'rb') as fin:
                # считываем количество блоков
                length = pickle.load(fin)

                for i in range(length):
                    # считываем позицию
                    pos = pickle.load(fin)

                    # создаём новый блок
                    self.add_block(pos)
        except IOError as err:
            print(f"Could not open/read file: {PATH_MAP}. {err}")
            sys.exit()
        except Exception as err:
            print("Unexpected error:", err)
            sys.exit()
