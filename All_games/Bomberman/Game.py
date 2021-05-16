import pygame as pg
from collections import deque
from random import *
from pygame.locals import *
from Bomber_man_obj import *

pg.init()
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (200, 200, 200)

# 0 - Пустая клутка
# 1 - Клетка с пробивной стеной
# 2 - Клетка с непробивной стеной
# 3 - Клетка с ГОРИЗОНТАЛЬНЫМ взрывом
# 4 - Клетка с ВЕРТИКАЛЬНЫМ взрывом
# 5 - клетка с бомбой
# 6 - центр взрыва
# 7 - случайный бонус

drawer = Drawer()

size = [400, 100]
size_of_cell = 30
screen = pg.display.set_mode(size)
f = 0
while 1:
    pg.draw.line(screen, WHITE, (100, 0), (100, 100), 5)
    pg.draw.line(screen, WHITE, (200, 0), (200, 200), 5)
    pg.draw.line(screen, WHITE, (300, 0), (300, 300), 5)
    pg.display.flip()

    if f == 1:
        break
    for event in pg.event.get():
        if event.type == QUIT:
            exit(0)
        if event.type == MOUSEBUTTONDOWN:
            kol_players = pg.mouse.get_pos()[0] // 100 + 1
            f = 1

size = [100, 100]
screen = pg.display.set_mode(size)
players = []
control = []
for i in range(kol_players):
    print('Нажмите: вверх, вниз, влево, вправо, кнопка для бомбы')
    controls = [0, 0, 0, 0, 0]
    l = 0
    se = set()
    pg.time.delay(1000)
    while 1:
        for event in pg.event.get():
            if event.type == QUIT:
                exit(0)

        keys = pg.key.get_pressed()
        for i in range(len(keys)):
            if keys[i]:
                if i in se:
                    break
                controls[l] = i
                se.add(i)
                l += 1
                break
        if controls[4]:
            break
    control.append(controls)


while 1:

    players = []
    for i in range(kol_players):
        players.append(Player(15, 15, control[i][0], control[i][1], control[i][2], control[i][3], control[i][4]))

    size = [600, 600]
    screen = pg.display.set_mode(size)
    clock = pg.time.Clock()
    background = pg.Surface(size).convert()
    num_of_event = 0

    a = [[0 for i in range(21)] for i in range(21)]
    for i in range(21):
        for j in range(21):
            chance = randrange(1, 101)

            if i == 20 or j == 20:
                a[i][j] = 2
                continue

            if 1 <= chance <= 30:
                a[i][j] = 2
            elif 31 <= chance <= 50:
                a[i][j] = 0
            else:
                a[i][j] = 1

    for player in players:
        player.position.x = randrange(15, 575) // size_of_cell * size_of_cell + 15
        player.position.y = randrange(15, 575) // size_of_cell * size_of_cell + 15
        i, j = get_index(player.position.y, player.position.x)
        a[i][j] = 0
        a[i][j + 1] = 0
        a[i][j - 1] = 0
        a[i + 1][j] = 0
        a[i - 1][j] = 0

    bg_color = (0, 0, 0)

    while 1: # как ты думаешь как у тебя дела

        for event in pg.event.get():
            if event.type == QUIT:
                exit(0)

        screen.blit(background, (0, 0))
        keys = pg.key.get_pressed()
        if keys[K_ESCAPE]:
            break

        for player in players:
            keys = pg.key.get_pressed()
            player.update(keys, a, players)
        update_a(a)

        drawer.draw_a(screen, a)
        for player in players:
            drawer.draw_player(screen, player)


        pg.display.flip()

        clock.tick(60)

