import pygame as pg
from random import *
from pygame.locals import *
from collections import deque
from Game_obj import *

# Инициализация
size_of_screen = (1366, 768)

n = int(input('Введите размеры поля '))
kol = int(input('Введите количество игроков '))

offsets = []
if kol == 1:
    offsets.append((size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 - size_of_cell * n // 2))
elif kol == 2:
    offsets.append((size_of_screen[0] // 2 // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 // 2 + size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 - size_of_cell * n // 2))
elif kol == 3:
    offsets.append((size_of_screen[0] // 2 // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 // 2 + size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 + size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
elif kol == 4:
    offsets.append((size_of_screen[0] // 2 // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 // 2 + size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 + size_of_screen[1] // 2 // 2 - size_of_cell * n // 2))
    offsets.append((size_of_screen[0] // 2 // 2 + size_of_screen[0] // 2 - size_of_cell * n // 2, size_of_screen[1] // 2 // 2 + size_of_screen[1] // 2 - size_of_cell * n // 2))

pg.init()

clock = pg.time.Clock()


# Настройка управления
size = [100, 100]
screen1 = pg.display.set_mode(size)
players = []
control = []
for i in range(kol):
    print('Нажмите: вверх, вниз, влево, вправо, Рестарт')
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

# Генерация карты
screen = 0
screen = pg.display.set_mode(size_of_screen, FULLSCREEN)
while 1:

    maps = []
    players = []

    map = Map(n + 1, (0, 0))
    map.generate()
    pi, pj = randrange(map.n - 1), randrange(map.n - 1)

    k = [[0 for _ in range(map.n)] for _ in range(map.n)]
    while not map.check(pi, pj, [[0 for _ in range(map.n)] for _ in range(map.n)], [], k):
        map.generate()
        map[pi][pj] = 0
    print(map.a, pi, pj)

    #map.a = [[1, 1, 1, 1, 1, 1], [0, 1, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1], [0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1], [1, 1, 1, 1, 1, 1]]
    
    #pi = 0
    #pj = 1
    #print(map.check(pi, pj, [[0 for _ in range(map.n)] for _ in range(map.n)], []))

    for i in range(kol):

        map_i = Map(n + 1, offsets[i])
        for i1 in range(n + 1):
            map_i.a[i1] = map.a[i1].copy()
        maps.append(map_i)
        players.append(Player(pi, pj, offsets[i]))
        players[i].set_controls(control[i])

# Игровой цикл
    f = 0
    while 1:

        if f == 1:
            f = 0
            break

        for event in pg.event.get():
            if event.type == QUIT:
                exit(0)

        # update
        for i in range(kol):
            keys = pg.key.get_pressed()
            if keys[players[i].restart]:
                players[i].i = pi
                players[i].j = pj
                for i1 in range(maps[i].n):
                    for j1 in range(maps[i].n):
                        if maps[i][i1][j1] == 2 or type(maps[i][i1][j1]) == Anim:
                            maps[i][i1][j1] = 0
            if keys[K_z]:
                if next_level(maps[0]):
                    f = 1
                    break

            if keys[K_DELETE]:
                f = 1
                break

            if keys[K_ESCAPE]:
                exit(0)
            keys = pg.key.get_pressed()
            players[i].key_update(keys)
            players[i].go_to(maps[i])
            maps[i].update()

        # draw
        screen.fill(WHITE)
        for map in maps:
            map.draw(screen)
        for player in players:
            player.draw(screen)

        pg.display.flip()

        clock.tick(60)
