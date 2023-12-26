from direct.showbase.ShowBase import ShowBase


from mapmanager import Mapmanager
from player import Player, Position
from conf import PATH_LAND
from camera import CameraControllerBehaviour


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x, y, _ = self.land.load_land(PATH_LAND)
        self.player = Player(Position(x // 2, y // 2, 2), self.land)
        self.camLens.setFov(90)
        # cam_controller = CameraControllerBehaviour(self.camera)
        # cam_controller.setMouseSensivity(0.9)
        # cam_controller.setup()
