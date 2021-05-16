import pygame as pg
from random import *
from pygame.locals import *
from collections import deque


# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (200, 200, 200)
GREEN = (100, 255, 100)
RED = (100, 0, 0)
BRIGHT_RED = (255, 0, 0)
ORANGE = (204, 102, 0)
BRAWN = (205, 133, 63)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GRASS = (0, 128, 0)

size_of_cell = 40

# Переменные


# Классы

class Map:
    def __init__(self, n, offset):
        self.a = [[0 for i in range(n)] for i in range(n)]
        self.offset = pg.math.Vector2()
        self.offset.x = offset[0]
        self.offset.y = offset[1]
        self.n = n

    def __getitem__(self, item):
        return self.a[item]

    def generate(self):
        for i in range(self.n):
            for j in range(self.n):
                if i == self.n - 1 or j == self.n - 1:
                    self[i][j] = 1
                else:
                    if 0 <= randrange(self.n) <= self.n // 5:
                        self[i][j] = 1
                    else:
                        self[i][j] = 0

    def draw(self, screen):
        for i in range(self.n - 1):
            for j in range(self.n - 1):
                x = j * size_of_cell + 3 + self.offset.x
                y = i * size_of_cell + 3 + self.offset.y
                if self[i][j] == 1:
                    pg.draw.line(screen, GRAY, (x, y + size_of_cell // 4), (x + size_of_cell // 4, y), 4)
                    pg.draw.line(screen, GRAY, (x, y + size_of_cell // 2), (x + size_of_cell // 2, y), 4)
                    pg.draw.line(screen, GRAY, (x + size_of_cell - size_of_cell // 2 - 7, y + size_of_cell - 7), (x + size_of_cell - 7, y + size_of_cell - size_of_cell // 2 - 7), 4)
                    pg.draw.line(screen, GRAY, (x + size_of_cell - size_of_cell // 4 - 7, y + size_of_cell - 7), (x + size_of_cell - 7, y + size_of_cell - size_of_cell // 4 - 7), 4)
                    pg.draw.line(screen, GRAY, (x, y + size_of_cell - 7), (x + size_of_cell - 7, y), 4)
                    pg.draw.rect(screen, BLACK, (x, y, size_of_cell - 6, size_of_cell - 6), 5)
                elif self[i][j] == 0:
                    pg.draw.rect(screen, SILVER, (x, y, size_of_cell - 6, size_of_cell - 6), 5)
                elif type(self[i][j]) == Anim:
                    pg.draw.rect(screen, GRASS, (x - 2, y - 2, size_of_cell - 2, size_of_cell - 2))
                elif self[i][j] == 2:
                    pg.draw.rect(screen, GRASS, (x, y, size_of_cell - 6, size_of_cell - 6), 5)
                    pg.draw.rect(screen, GREEN, (x + 2, y + 2, size_of_cell - 10, size_of_cell - 10))

    def update(self):
        for i in range(self.n):
            for j in range(self.n):
                if type(self[i][j]) == Anim:
                    if pg.time.get_ticks() - self[i][j].start_time > 150:
                        self[i][j] = 2

    def check(self, i, j, used, path, kol):

  #      used = []
   #     for i1 in range(len(use)):
    #        used.append(use[i1].copy())


        se = set()
        if self.go_to(used, 1, 0, i, j, path, kol):
            return 1
        if self.go_to(used, -1, 0, i, j, path, kol):
            return 1
        if self.go_to(used, 0, 1, i, j, path, kol):
            return 1
        if self.go_to(used, 0, -1, i, j, path, kol):
            return 1
        for i in range(len(used)):
            for j in range(len(used)):
                if used[i][j] == 0 and self[i][j] != 1:
                    se.add((i, j))
        if len(se) < 3:
            for ij in list(se):
                i, j = ij
                self[i][j] = 1

                for i in range(len(path)):
                    print(str(path[i][0]) + str(path[i][1]) + ' ')
                print()

            return 1
        else:
            return 0

    def go_to(self, used, di, dj, i, j, path, k):

        while self[di + i][dj + j] != 1:
            used[i][j] = 1
            i += di
            j += dj
        if used[i][j] == 0:
            used[i][j] = 1
            self.check(i, j, used, path + [[di, dj]], k)
      #  else:
       #     if k[i][j] <= 2:
        #        k[i][j] += 1
         #       self.check(i, j, used, path + [[di, dj]], k)


class Player:
    def __init__(self, i, j, offset):
        self.i = i
        self.j = j
        self.offset = pg.math.Vector2()

        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.restart = None

        self.offset.x = offset[0]
        self.offset.y = offset[1]
        self.direction = None

    def key_update(self, keys):
        if not self.direction:
            if keys[self.down]:
                self.direction = 'down'
            elif keys[self.up]:
                self.direction = 'up'
            elif keys[self.right]:
                self.direction = 'right'
            elif keys[self.left]:
                self.direction = 'left'

    def go_to(self, map):
        di = 0
        dj = 0
        if self.direction == 'left':
            dj = -1
        elif self.direction == 'right':
            dj = 1
        elif self.direction == 'up':
            di = -1
        elif self.direction == 'down':
            di = 1

        map[self.i][self.j] = Anim(pg.time.get_ticks())
        if map[self.i + di][self.j + dj] == 1:
            self.direction = None
            di = 0
            dj = 0

        self.i += di
        self.j += dj

    def draw(self, screen):
        pg.draw.rect(screen, (GRASS[0], GRASS[1] - 50, GRASS[2]), (self.j * size_of_cell + 5 + self.offset.x, self.i * size_of_cell + 5 + self.offset.y, size_of_cell - 10, size_of_cell - 10))

    def set_controls(self, controls):
        self.up = controls[0]
        self.down = controls[1]
        self.left = controls[2]
        self.right = controls[3]
        self.restart = controls[4]


class Anim:
    def __init__(self, start_time):
        self.start_time = start_time


def next_level(map):
    for i in range(map.n):
        for j in range(map.n):
            if map[i][j] == 0:
                return 0
    return 1
