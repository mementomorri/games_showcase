from pygame import display

from conf import WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR

window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # window interface to reference
display.set_caption('ping-pong')  # can be refactored with singleton
window.fill(BACKGROUND_COLOR)
