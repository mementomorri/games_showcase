from conf import *
from type_hints import Position, IMapmanager, degrees


class Player:
    def __init__(self, position: Position, land: IMapmanager) -> None:
        """
        Representation of player controlled actor.
        :param position: Position - coordinates representation implemented with tuple.
        :param land:
        """
        self.land = land
        self.mode = False  # режим прохождения сквозь объекты
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(*PLAYER_COLOR)
        self.hero.setScale(PLAYER_SCALE)
        self.hero.setH(PLAYER_HORIZONTAL_POSITION)
        self.hero.setPos(position)
        self.hero.reparentTo(render)
        self._camera_bind()
        self._accept_events()

    def _camera_bind(self) -> None:
        base.disableMouse()
        base.camera.reparentTo(self.hero)
        base.camera.setPos(*CAMERA_START_POSITION)
        self.cameraOn = True

    def _camera_up(self) -> None:
        position = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-position[0], -position[1], -position[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def _change_view(self) -> None: self._camera_up() if self.cameraOn else self._camera_bind()

    def _turn_left(self) -> None: self.hero.setH((self.hero.getH() + PLAYER_TURN_DEGREE) % 360)

    def _turn_right(self) -> None: self.hero.setH((self.hero.getH() - PLAYER_TURN_DEGREE) % 360)

    def _look_at(self, angle: degrees) -> Position:
        """ возвращает координаты, в которые переместится персонаж, стоящий в точке (x, y),
        если он делает шаг в направлении angle"""

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy, _ = self._check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return Position(x_to, y_to, z_from)

    def _update_pos(self, angle: degrees) -> None: self.hero.setPos(self._look_at(angle))

    @staticmethod
    def _check_dir(angle: degrees) -> Position:
        """ возвращает округленные изменения координат X, Y,
        соответствующие перемещению в сторону угла angle.
        Координата Y уменьшается, если персонаж смотрит на угол 0,
        и увеличивается, если смотрит на угол 180.
        Координата X увеличивается, если персонаж смотрит на угол 90,
        и уменьшается, если смотрит на угол 270.
            угол 0 (от 0 до 20)      ->        Y - 1
            угол 45 (от 25 до 65)    -> X + 1, Y - 1
            угол 90 (от 70 до 110)   -> X + 1
            от 115 до 155            -> X + 1, Y + 1
            от 160 до 200            ->        Y + 1
            от 205 до 245            -> X - 1, Y + 1
            от 250 до 290            -> X - 1
            от 290 до 335            -> X - 1, Y - 1
            от 340                   ->        Y - 1  """
        if 0 <= angle <= 20:
            return Position(0, -1, None)
        elif angle <= 65:
            return Position(1, -1, None)
        elif angle <= 110:
            return Position(1, 0, None)
        elif angle <= 155:
            return Position(1, 1, None)
        elif angle <= 200:
            return Position(0, 1, None)
        elif angle <= 245:
            return Position(-1, 1, None)
        elif angle <= 290:
            return Position(-1, 0, None)
        elif angle <= 335:
            return Position(-1, -1, None)
        else:
            return Position(0, -1, None)

    def _forward(self) -> None: self.move_to((self.hero.getH() + 180) % 360)

    def _back(self) -> None: self.move_to((self.hero.getH()) % 360)

    def _left(self) -> None: self.move_to((self.hero.getH() + 270) % 360)

    def _right(self) -> None: self.move_to((self.hero.getH() + 90) % 360)

    def _switch_mode(self) -> None: self.mode = not self.mode

    def _try_move(self, angle: degrees) -> None:
        """перемещается, если может"""
        position = self._look_at(angle)
        if self.land.is_empty(position):
            # перед нами свободно. Возможно, надо упасть вниз:
            position = self.land.find_highest_empty(position)
            self.hero.setPos(position)
        else:
            # перед нами занято. Если получится, заберёмся на этот блок:
            position = Position(position[0], position[1], position[2] + 1)
            if self.land.is_empty(position):
                self.hero.setPos(position)
                # не получится забраться - стоим на месте

    def _up(self) -> None:
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def _down(self) -> None:
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

    def _build(self) -> None:
        angle = self.hero.getH() % 180
        position = self._look_at(angle)
        if self.mode:
            self.land.add_block(position)
        else:
            self.land.build_block(position)

    def _destroy(self) -> None:
        angle = self.hero.getH() % 180
        position = self._look_at(angle)
        if self.mode:
            self.land.del_block(position)
        else:
            self.land.del_block_from(position)

    def _accept_events(self) -> None:
        base.accept(KEY_TURN_LEFT, self._turn_left)
        base.accept(KEY_TURN_LEFT + '-repeat', self._turn_left)
        base.accept(KEY_TURN_RIGHT, self._turn_right)
        base.accept(KEY_TURN_RIGHT + '-repeat', self._turn_right)

        base.accept(KEY_MOVE_BACK, self._forward)
        base.accept(KEY_MOVE_BACK + '-repeat', self._forward)
        base.accept(KEY_MOVE_FORWARD, self._back)
        base.accept(KEY_MOVE_FORWARD + '-repeat', self._back)
        base.accept(KEY_MOVE_LEFT, self._left)
        base.accept(KEY_MOVE_LEFT + '-repeat', self._left)
        base.accept(KEY_MOVE_RIGHT, self._right)
        base.accept(KEY_MOVE_RIGHT + '-repeat', self._right)

        base.accept(KEY_SWITCH_CAMERA, self._change_view)
        base.accept(KEY_SWITCH_MODE, self._switch_mode)

        base.accept(KEY_MOVE_UP, self._up)
        base.accept(KEY_MOVE_UP + '-repeat', self._up)
        base.accept(KEY_MOVE_DOWN, self._down)
        base.accept(KEY_MOVE_DOWN + '-repeat', self._down)

        base.accept(KEY_BUILD_BLOCK, self._build)
        base.accept(KEY_DESTROY_BLOCK, self._destroy)

        base.accept(KEY_SAVE_MAP, self.land.save_map)
        base.accept(KEY_LOAD_MAP, self.land.load_map)

    def move_to(self, angle: degrees) -> None: self._update_pos(angle) if self.mode else self._try_move(angle)
