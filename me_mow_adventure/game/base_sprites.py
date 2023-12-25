import pygame
from constants import *
from gamesingle import game
from type_hints import Coordinate, Speed


class BaseSprite(pygame.sprite.Sprite):
    """ Корневой класс для наследования классами персонажей.
    :param image  картинка персонажа, тип Surface;
    :param coord  координата появления персонажа по оси координат x и y, тип Coordinate;
    :param speed  длинна шага персонажа (в пикселях), который спрайт проходит за один раз, тип Speed;
    :param area  "место обитания" - готовый прямоугольник (pygame rect),
    внутри которого спрайт должен оставаться, тип pygame.Rect.
     """

    # конструктор :
    def __init__(self, image: pygame.Surface, coord: Coordinate, area: pygame.Rect,
                 speed: Speed = Speed(0, 0)) -> None:
        # Вызываем конструктор класса (Sprite):
        super().__init__()

        # каждый спрайт должен хранить свойство image - картинку. Берем переданную в виде параметра конструктора:
        self.image = image
        # каждый спрайт должен хранить свойство rect - прямоугольник. Это свойство нужно преждевсего
        # для определения касаний спрайтов.
        self.rect = self.image.get_rect()
        self.rect.x = coord.x
        self.rect.y = coord.y

        self.area = area
        self.x_speed = speed.x
        self.y_speed = speed.y
        # для спрайтов смешавшихся вместе с этим спрайтом, нужно знать, насколько спрайту удалось
        # переместиться за последний циккл отрисовки кадра:
        self.x_changed = 0
        self.y_changed = 0
        # направление движения по горизонтали: вправо = 1, влево = -1 :
        self.direction = 1
        if self.x_speed < 0:
            self.direction = -1

    def change_dir(self) -> None:
        """
        Смена направления движения спрайта по горизонтали на противоположное.
        :rtype: None
        """
        self.x_speed *= -1
        self.direction *= -1

    def change_ydir(self) -> None:
        """
        Смена направления движения спрайта по вертикали на противоположное.
        :rtype: None
        """
        self.y_speed *= -1

    def outside(self) -> bool:
        """
        Проверяет, не вышел ли спрайт за пределы отведенного ему ареала.
        """
        return not self.area.contains(self.rect)

    def update(self) -> None:
        """
        Метод изменения позиции; может быть вызыван из группы спрайтов.
        Сначала применяет изменение по x,
        проверяет корректность текущего положения,
        затем применяет изменение по y и тоже проверяет корректность этго положения.
        """
        self.rect.x += self.x_speed
        self.x_changed = self.x_speed

        if self.outside():
            self.rect.x -= self.x_speed
            self.x_changed = 0
            self.change_dir()

        self.rect.y += self.y_speed
        self.y_changed = self.y_speed
        if self.outside():
            self.rect.y -= self.y_speed
            self.y_changed = 0
            self.change_ydir()


class Character(BaseSprite):
    """
    Класс репрезентация игровового персонажа.
    :param heavy  число пикселей, на которые персонаж падает вниз, тип int:
    :param die_x  умирает ли персонаж, если оказывается вне ареала по оси абсцисс
    (снаряды умирают по умолчанию), тип bool;
    :param die_y  умирает ли персонаж, если оказывается ВНИЗУ ареала
    (считаем, что вверху никогда не умирает, просто возвращается вниз), тип bool;
    :param graph_index  индекс костюма персонажа, тип int.
    """

    def __init__(self, image: pygame.Surface, coord: Coordinate, area: pygame.Rect,
                 speed: Speed = Speed(0, 0), die_x: bool = False, die_y: bool = True, heavy: int = GRAVITY,
                 graph_index=gr_hero):
        # конструктор базового класса
        super().__init__(image, coord, area, speed)
        # старое направление движения
        self.old_direction = 0

        self.die_x = die_x
        self.die_y = die_y
        self.heavy = heavy
        self.graph_index = graph_index
        # Ссылка на платформу, на которой стоит персонаж
        self.stands_on = None

    def check_dir(self) -> None:
        """
        Проверка смены направления движения. Обновляет картинку, если это так.
        """
        if self.old_direction != self.direction:
            if self.direction > 0:
                self.image = game.costumes[self.graph_index]
            else:
                self.image = game.costumes[self.graph_index + gr_total]  # вторая копия списка содержит зеркальные копии
        self.old_direction = self.direction  # обработали и запомнили

    def gravitate(self) -> None:
        """
        Имитация воздействия гравитации на объект.
        """
        self.y_speed += self.heavy

    def die(self) -> None:
        """
        'Убивает' персонажа
        """
        self.kill()  # можно поменять во время анимацию гибели персонажа!

    def update(self) -> None:
        """
        Метод обновления положения объекта.
        1. проверяет, столкнулись ли платформы с персонажем;
        2. перемещения всех платформ двигают и персонажа в том числе;
        3. имитация гравитации;
        4. обновление полохожения по оси x и по оси y;
        5. после изменений по оси x проверяет на выход объекта за пределы "ареала";
        6. после изменений по y тпроверяет на выход объекта за пределы "ареала",
        но с учетом приземления на барьер.
        """

        # Для совместимости с базовым классом тоже будем подсчитывать x_changed и y_changed:
        old_x = self.rect.x
        old_y = self.rect.y

        # 1. Проверяем на столкнавение и расталкиваем столкнувшиеся платформы.
        # Применяем изменения координат платформ, которых коснулись.
        platforms_touched = pygame.sprite.spritecollide(self, game.barriers, False)
        for p in platforms_touched:
            self.rect.x += p.x_changed
            self.rect.y += p.y_changed
        # 2. Платформы, на которой персонаж стоит, он может не касаться, но она должна двигать персонажа точно так же:
        if self.stands_on and self.stands_on not in platforms_touched:
            p = self.stands_on
            self.rect.x += p.x_changed
            self.rect.y += p.y_changed
        # Если после всех преобразований персонаж все еще касается какого-то объекта, значит, его раздавило!
        platforms_touched = pygame.sprite.spritecollide(self, game.barriers, False)
        if len(platforms_touched) > 0:
            self.die()

        # 3. Имитация гравитации.
        self.gravitate()
        # теперь в x_speed и y_speed те изменения, которые нужно применить

        # 4. Теперь движение самого спрайта. Сначала учитываем изменение по x:
        self.rect.x += self.x_speed

        # Если зашли за стенку, то встанем вплотную к стене
        platforms_touched = pygame.sprite.spritecollide(self, game.barriers, False)
        if self.x_speed > 0:  # идем направо, правый край персонажа - вплотную к левому краю стены
            for p in platforms_touched:
                self.rect.right = min(self.rect.right,
                                      p.rect.left)
        elif self.x_speed < 0:  # идем налево, ставим левый край персонажа вплотную к правому краю стены
            for p in platforms_touched:
                self.rect.left = max(self.rect.left,
                                     p.rect.right)  # если коснулись нескольких стен, то левый край - максимальный

        # Проверяем, на вхождение в пределы ареала:
        if self.outside():
            if self.die_x:
                self.die()
            else:
                self.rect.x -= self.x_speed
                self.change_dir()

        # 6. Теперь изменения по y:
        self.rect.y += self.y_speed

        # Проверим, не ушел ли персонаж с платформы, на которой стоял:
        if self.stands_on:
            if (
                    self.y_speed < 0  # оттолкнулись от платформы и ушли на y_speed относительно неё
                    or self.rect.right < self.stands_on.rect.left  # оказались левее левого края опоры
                    or self.rect.left > self.stands_on.rect.right  # оказались правее опоры
            ):
                self.stands_on = False  # больше ни на чем не стоим

        # Проверим, не коснулись ли платформ:

        platforms_touched = pygame.sprite.spritecollide(self, game.barriers, False)

        if self.y_speed > 0:  # идем вниз
            for p in platforms_touched:
                if self.heavy > 0:
                    self.y_speed = 0  # при касании с препятствием по y вертикальная скорость пропадает
                # персонаж, который управляется не гравитацией, а "ареалом", продолжает попытки пройти
                # проверяем, какая из платформ снизу самая высокая, выравниваемся по ней, запоминаем её как свою опору
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
                    self.stands_on = p

        elif self.y_speed < 0:  # идем вверх
            self.stands_on = False  # пошли наверх, значит, ни на чем уже не стоим!
            for p in platforms_touched:
                if self.heavy > 0:
                    self.y_speed = 0  # при касании с препятствием по y вертикальная скорость пропадает:
                self.rect.top = max(self.rect.top,
                                    p.rect.bottom)  # выравниваем верхний край по нижним краям стенок, на которые
                # наехали

        # Проверка выхода за пределы ареала:

        if self.outside():
            if self.die_y and self.rect.bottom > self.area.bottom:
                # провалились вниз:
                self.die()
            else:
                self.rect.y -= self.y_speed
                self.change_ydir()

        # Запомнили изменения (завершение п.1)
        self.x_changed = old_x - self.rect.x
        self.y_changed = old_y - self.rect.y

        # Отображает зеркально, если нужно
        self.check_dir()
