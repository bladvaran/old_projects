# 16 x 16     30 bomb

from collections import deque
import pygame
import random
pygame.init()
pygame.font.init()

num = pygame.font.SysFont('Comic Sans MS', 25, 1)

h = 500
w = 500


def kordi(i, j):
    return [i * 30 - 23, j * 30 - 12]


def pos(x, y):
    return [(x + 20) // 30, (y + 20) // 30]


def gener():
    bombs = []
    for i in range(40):
        bombs.append([random.randrange(1, 17), random.randrange(1, 17)])
    pole = [[Kletka() for i in range(18)] for j in range(18)]

    for i in range(18):
        pole[0][i].bomb = -1
        pole[17][i].bomb = -1
        pole[i][0].bomb = -1
        pole[i][17].bomb = -1

        pole[0][i].num = 1
        pole[17][i].num = 1
        pole[i][0].num = 1
        pole[i][17].num = 1

    for i in range(40):
        pole[bombs[i][0]][bombs[i][1]].bomb = 1
        pole[bombs[i][0]][bombs[i][1]].num = -1
    k = 0
    for i in range(1, 17):
        for j in range(1, 17):
            if pole[i][j].bomb == 0:
                for s in range(-1, 2):
                    for c in range(-1, 2):
                        if pole[i + s][j + c].bomb == 1:
                            k += 1
            pole[i][j].num = k
            k = 0
    return pole


class Pole():

    def __init__(self):
        self.pole = gener()

    def draw(self, screen):
        x_r = 40
        y_r = 40
        pygame.draw.rect(screen, (0, 0, 0), (10, 10, w - 20, h - 20), 3)
        for i in range(15):
            pygame.draw.line(screen, (0, 0, 0), (x_r, 10), (x_r, h - 10), 2)
            x_r += 30
        for i in range(15):
            pygame.draw.line(screen, (0, 0, 0), (10, y_r), (w - 10, y_r), 2)
            y_r += 30

        x_r = 12
        y_r = 12

        for i in range(1, 17):
            for j in range(1, 17):
                if self.pole[i][j].open == 0:
                    pygame.draw.rect(screen, (100, 100, 200), (x_r, y_r, 26, 26))
                else:
                    if self.pole[i][j].num != 0:
                        pygame.draw.rect(screen, (200, 200, 200), (x_r, y_r, 26, 26))
                        screen.blit((num.render(str(self.pole[i][j].num), False, (255, 0, 0))), (kordi(i, j)[1], kordi(i, j)[0]))
                    else:
                        pygame.draw.rect(screen, (250, 250, 250), (x_r, y_r, 26, 26))
                if self.pole[i][j].flag == 1:
                    screen.blit((num.render('!', False, (0, 255, 0))), (kordi(i, j)[1], kordi(i, j)[0]))
                x_r += 30
            y_r += 30
            x_r = 12

    def update(self, mouse, key, key1):

        y, x = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        x, y = pos(x, y)[0], pos(x, y)[1]
        if mouse[0]:
            if self.pole[x][y].bomb == 1 and not self.pole[x][y].flag:
                return 1
            if (self.pole[x][y].open == 0) and (self.pole[x][y].num == 0):

                Pole.bfs(self, x, y)
            else:
                self.pole[x][y].open = 1
        if (key[pygame.K_SPACE] and not key1[pygame.K_SPACE]) or (mouse[2]):
            pygame.time.wait(150)
            if self.pole[x][y].open == 0:
                if self.pole[x][y].flag == 0:
                    self.pole[x][y].flag = 1
                else:
                    self.pole[x][y].flag = 0

    def bfs(self, i, j):
        q = deque()
        q.append([i, j])
        self.pole[i][j].open = 1
        while len(q) > 0:
            x, y = q[0][0], q[0][1]
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if self.pole[x + j][y + i].open == 0:
                        if self.pole[x + j][y + i].num == 0:
                            q.append([x + j, y + i])
                            self.pole[x + j][y + i].open = 1
                        elif self.pole[x + j][y + i].bomb == 0:
                            self.pole[x + j][y + i].open = 1
            q.popleft()


class Kletka():

    def __init__(self):
        self.open = 0
        self.bomb = 0
        self.num = 0
        self.flag = 0
