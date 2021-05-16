import pygame
import random
pygame.init()

w = 500
h = 500

def men(a):
    if a == 'P1':
        return 'P2'
    else:
        return 'P1'


def kordi(i, j):
    return [50 + 133 * i, 50 + 133 * j]


class Pole():

    def __init__(self):
        self.pole = [[Kletka() for i in range(3)] for j in range(3)]
        self.vibor = {'x': 0, 'y': 0}
        self.hod = 'P1'
        self.end = 0
        self.direction = 0
        self.k = 100

    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (180, 50), (180, h - 50), 6)
        pygame.draw.line(screen, (0, 0, 0), (w - 180, 50), (w - 180, h - 50), 6)
        pygame.draw.line(screen, (0, 0, 0), (50, 180), (w - 50, 180), 6)
        pygame.draw.line(screen, (0, 0, 0), (50, w - 180), (w - 50, h - 180), 6)
        for i in range(3):
            for j in range(3):
                x = kordi(i, j)[0]
                y = kordi(i, j)[1]
                if self.pole[i][j].pusto == 'Cross':
                    pygame.draw.line(screen, (255, 20, 0), (x + 30, y + 30), (x + 100, y + 100), 5)
                    pygame.draw.line(screen, (255, 20, 0), (x + 100, y + 30), (x + 30, y + 100), 5)
                elif self.pole[i][j].pusto == 'Circle':
                    pygame.draw.circle(screen, (255, 20, 0), (x + 65, y + 65), 40, 4)
        x = kordi(self.vibor['x'], self.vibor['y'])[0] + 20
        y = kordi(self.vibor['x'], self.vibor['y'])[1] + 20
        if self.end == 0:
            pygame.draw.rect(screen, (0, 20, 100), (x, y, 20, 20))

    def update(self, key, key1, screen):
        if self.end == 0:
            if self.hod == 'P1':
                if key[pygame.K_w] and not(key1[pygame.K_w]) and self.vibor['y'] != 0:
                    self.vibor['y'] -= 1
                if key[pygame.K_a] and not(key1[pygame.K_a]) and self.vibor['x'] != 0:
                    self.vibor['x'] -= 1
                if key[pygame.K_s] and not(key1[pygame.K_s]) and self.vibor['y'] != 2:
                    self.vibor['y'] += 1
                if key[pygame.K_d] and not(key1[pygame.K_d]) and self.vibor['x'] != 2:
                    self.vibor['x'] += 1
                if key[pygame.K_SPACE] and not(key1[pygame.K_SPACE]):
                    if self.pole[self.vibor['x']][self.vibor['y']].pusto == 1:
                        self.pole[self.vibor['x']][self.vibor['y']].pusto = 'Cross'
                        self.hod = 'P2'
            else:
                if key[pygame.K_UP] and not(key1[pygame.K_UP]) and self.vibor['y'] != 0:
                    self.vibor['y'] -= 1
                if key[pygame.K_LEFT] and not(key1[pygame.K_LEFT]) and self.vibor['x'] != 0:
                    self.vibor['x'] -= 1
                if key[pygame.K_DOWN] and not(key1[pygame.K_DOWN]) and self.vibor['y'] != 2:
                    self.vibor['y'] += 1
                if key[pygame.K_RIGHT] and not(key1[pygame.K_RIGHT]) and self.vibor['x'] != 2:
                    self.vibor['x'] += 1
                if key[pygame.K_SLASH] and not(key1[pygame.K_SLASH]):
                    if self.pole[self.vibor['x']][self.vibor['y']].pusto == 1:
                        self.pole[self.vibor['x']][self.vibor['y']].pusto = 'Circle'
                        self.hod = 'P1'
        else:
            if self.direction == 'H':
                Pole.horizontal(self, self.k, self.vibor['x'], screen)
            elif self.direction == 'V':
                Pole.vertical(self, self.k, self.vibor['y'], screen)
            elif self.direction == 'D1':
                Pole.d1(self, self.k, screen)
            elif self.direction == 'D2':
                Pole.d2(self, self.k, screen)
            self.k += 10
        k = 0
        n = 0
        l = 0
        for i in range(3):
            for j in range(3):
                if self.pole[i][j].pusto != 1:
                    l += 1
                if self.pole[i][j].pusto == 'Cross':
                    k += 1
                elif self.pole[i][j].pusto == 'Circle':
                    n += 1
                if (k == 3) or (n == 3):
                    self.end = 1
                    self.direction = 'H'

            k = 0
            n = 0
        if l == 9:
            self.k = 401

        for i in range(3):
            for j in range(3):
                if self.pole[j][i].pusto == 'Cross':
                    k += 1
                elif self.pole[j][i].pusto == 'Circle':
                    n += 1
                if (k == 3) or (n == 3):
                    self.end = 1
                    self.direction = 'V'
            k = 0
            n = 0

        if (self.pole[0][0].pusto == self.pole[1][1].pusto == self.pole[2][2].pusto) and (self.pole[0][0].pusto != 1):
            self.end = 1
            self.direction = 'D1'
        if (self.pole[0][2].pusto == self.pole[1][1].pusto == self.pole[2][0].pusto) and (self.pole[1][1].pusto != 1):
            self.end = 1
            self.direction = 'D2'

    def vertical(self, k, y, screen):
        pygame.draw.line(screen, (255, 0, 0), (100, y + 110), (k, y + 110), 10)

    def horizontal(self, k, x, screen):
        pygame.draw.line(screen, (255, 0, 0), (x + 110, 100), (x + 110, k), 10)

    def d1(self, k, screen):
        pygame.draw.line(screen, (255, 0, 0), (100, 100), (k, k), 10)

    def d2(self, k, screen):
        pygame.draw.line(screen, (255, 0, 0), (w - 100, 100), (w - k, k), 10)


class Kletka():

    def __init__(self):
        self.pusto = 1
