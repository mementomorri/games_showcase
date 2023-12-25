# from . import game
from .gamesingle import game
from .game_sprites import *


def game_loop() -> None:
    game.start()
    hero = game.start_level(0)

    game.show_menu()

    key_a = pygame.K_a
    key_d = pygame.K_d
    key_h = pygame.K_h  # режим help включается по отжатию клавиши h
    while game.run:
        # Ввод данных (обработка событий)
        for event in pygame.event.get():
            # событие нажатия на кнопку 'выйти'
            if event.type == pygame.QUIT:
                game.stop()  # корректное завершение работы программы
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # завершение работы программы, при нажатии клавиши 'esc'
                    game.stop()
                # elif event.key == pygame.K_r:  # restart game all over
                #     game.restart()
                elif event.key == pygame.K_LEFT:
                    hero.move_left(HERO_STEP)
                elif event.unicode == 'a':  # повторная проверка нажатия клавиш, чтобы избежать ошибки кодировки
                    hero.move_left(HERO_STEP)
                    key_a = event.key
                elif event.key == pygame.K_RIGHT:
                    hero.move_right(HERO_STEP)
                elif event.unicode == 'd':
                    hero.move_right(HERO_STEP)
                    key_d = event.key
                elif event.key == pygame.K_UP or event.unicode == 'w':
                    hero.jump(HERO_JUMP)
                elif event.unicode == 'h':
                    key_h = event.key
                elif event.unicode == 'm':
                    game.music.change()
                elif event.unicode == '+':
                    game.music.volume_up()
                elif event.unicode == '-':
                    game.music.volume_down()
                elif event.key == pygame.K_SPACE:
                    game.music.good_fire()
                    hero.fire()

            elif event.type == pygame.KEYUP:
                if game.is_help:
                    game.resume()
                else:
                    if event.key == pygame.K_LEFT or event.key == key_a:
                        hero.stop()
                    elif event.key == pygame.K_RIGHT or event.key == key_d:
                        hero.stop()
                    elif event.key == key_h:
                        game.show_menu()

        if game.in_game():
            game.all_sprites.update()

            # проверка на необходимость смещения "камеры", перед тем как отрисовывать следующий кадр
            if hero.rect.left < win_leftbound or hero.rect.right > win_rightbound:
                offset_x = game.hero_pos.x - hero.rect.x
                game.camera.move(offset_x, 0, game.all_sprites)
            # назначение текущего положения "камеры" как полежение персонажа в текущий момент
            game.hero_pos.x = hero.rect.x
            game.hero_pos.y = hero.rect.y

            # отрисовка
            game.draw_back_with_shift()
            game.window.blit(game.help.line(points=game.points, lives=game.lives), (0, 10))
            game.all_sprites.draw(game.window)

        pygame.display.update()
        if game.goal_touched(hero):  # условие завершения уровня
            game.next_level()

        if hero not in game.all_sprites:  # условие провала на уровне
            if game.lives > 0:
                # restart level at this point
                game.timer.tick(1)
                hero = game.restart_level()
            else:
                game.lose()

        game.timer.tick(FPS)


# if __name__ == '__main__':
#     main()
