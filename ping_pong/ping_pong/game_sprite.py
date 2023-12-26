from pygame import transform, image, Surface, sprite
import base64
from io import BytesIO
from PIL import Image

from type_hints import *
from window_interface import window


def pil_image_to_surface(pil_image: Image) -> Surface:
    """
    Convenient function to process bstring and transform it to Image.
    :param pil_image: image of game sprite
    :return: surface to draw
    """
    return image.fromstring(
        pil_image.tobytes(), pil_image.size, pil_image.mode)


class GameSprite(sprite.Sprite):
    def __init__(self, picture_bytestring: str, sprite_position: SpriteCoordinates,
                 movement_velocity: int, sprite_size: SpriteSize) -> None:
        """
        Parent class for game sprites, used for visualisation of simple objects.
        :param picture_bytestring: byte string representation of image.
        :param sprite_position: sprite start position (x, y).
        :param movement_velocity: amount of pixels sprite moves with.
        :param sprite_size: sprite size in pixels (width, height).
        """
        super().__init__()
        image_data = Image.open(BytesIO(base64.b64decode(picture_bytestring)))
        pygame_image = pil_image_to_surface(image_data)
        self.image = transform.scale(pygame_image, sprite_size)
        self.rect = self.image.get_rect()
        self.speed = movement_velocity
        # self.rectx, self.rect.y = sprite_position
        self.rect.x = sprite_position[0]
        self.rect.y = sprite_position[1]

    def reset(self) -> None:
        """
        Blit sprite at it's current position.
        """
        window.blit(self.image, (self.rect.x, self.rect.y))
