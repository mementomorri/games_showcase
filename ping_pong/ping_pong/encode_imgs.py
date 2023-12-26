import base64
from pathlib import Path
# from pygame import image

from conf import BALL_PATH, RACKET_PATH


def img_to_str(img: Path, store_name: str) -> None:
    """
    This function used to convert image to bse64 string. Mostly used for executable file generation.
    :param img: path to image.
    :param store_name: variable to store in output file.
    """
    with open(img, 'rb') as pic:
        content = '{} = {}\n'.format(store_name, base64.b64encode(pic.read()))

    with open('images_b64.py', 'a') as f:
        f.write(content)


if __name__ == '__main__':  # generate bstring when necessary with this entry point
    img_to_str(Path('../'+BALL_PATH), 'ball')
    img_to_str(Path('../'+RACKET_PATH), 'racket')


