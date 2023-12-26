from pygame import key, K_UP, K_DOWN, K_w, K_s

from game_sprite import GameSprite
from conf import WINDOW_HEIGHT, RACKET_HEIGHT, UPPER_WINDOW_MARGIN


class Racket(GameSprite):
    def update_right_racket(self) -> None:
        """
        Update right racket current position considering keys pressed.
        """
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > UPPER_WINDOW_MARGIN:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < WINDOW_HEIGHT - RACKET_HEIGHT:
            self.rect.y += self.speed

    def update_left_racket(self) -> None:
        """
        Update left racket current position considering keys pressed.
        """
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > UPPER_WINDOW_MARGIN:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < WINDOW_HEIGHT - RACKET_HEIGHT:
            self.rect.y += self.speed
