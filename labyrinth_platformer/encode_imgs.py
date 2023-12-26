import base64


def img2str(img: str, store_name: str) -> None:
    """
    Функция конвертации изображений в бинарные строки. Нужна для конвертации изображений в код игры,
    чтобы Pyinstaller собрал исполняемый файл вместе с изображениями.
    :param img: путь к изображению
    :param store_name: имя переменной для хранения во внешнем файле img2str.py
    """
    pic = open(img, 'rb')
    content = '{} = {}\n'.format(store_name, base64.b64encode(pic.read()))
    pic.close()

    with open('img2str.py', 'a') as f:
        f.write(content)


if __name__ == '__main__':
    img2str('img/background.jpg', 'background')
    img2str('img/bullet.png', 'bullet')
    img2str('img/fail_pic.png', 'fail_pic')
    img2str('img/finish.png', 'finish')
    img2str('img/obstacle.png', 'obstacle')
    img2str('img/player.png', 'player')
    img2str('img/victory_pic.png', 'victory_pic')
    img2str('img/wall_1.jpg', 'wall_1')
    img2str('img/wall_2.jpg', 'wall_2')
    img2str('img/wall_3.jpg', 'wall_3')

