import random
import pygame
pygame.init()
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)

h = 600
w = 600


def kordi(i, j):
    return {'x': i * 125 + 112, 'y': j * 125 + 112}


class Pole:

    def __init__(self):
        self.pole = [[Kletka() for i in range(4)] for j in range(4)]


    def draw_p(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (50, 50, 500, 500), 2)
        x = 175
        y = 175
        for i in range(3):
            pygame.draw.line(screen, (100, 100, 100), (x, 50), (x, 550), 2)
            x += 125

        for i in range(3):
            pygame.draw.line(screen, (100, 100, 100), (50, y), (550, y), 2)
            y += 125

        for i in range(4):
            for j in range(4):
                if self.pole[i][j].pusto == 0:
                    screen.blit(myfont.render(str(self.pole[i][j].chislo), False, (0, 0, 0)),
                                (kordi(i, j)['y'], kordi(i, j)['x']))

    def update(self, key1, key2):
        if key1[pygame.K_LEFT] and not(key2[pygame.K_LEFT]):
            dir = 'left'
            k = -1
        elif key1[pygame.K_UP] and not(key2[pygame.K_UP]):
            dir = 'up'
            k = -1
        elif key1[pygame.K_RIGHT] and not(key2[pygame.K_RIGHT]):
            dir = 'right'
            k = 1
        elif key1[pygame.K_DOWN] and not(key2[pygame.K_DOWN]):
            dir = 'down'
            k = 1
        else:
            return

        global p
        p = [[1 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                p[i][j] = self.pole[i][j].pusto

        if dir == 'up' or dir == 'left':
            for i in range(4):
                for j in range(4):
                    if self.pole[i][j].pusto == 0:
                        Pole._delo(self, i, j, dir, k)
        else:
            for i in range(3, -1, -1):
                for j in range(3, -1, -1):
                    if self.pole[i][j].pusto == 0:
                        Pole._delo(self, i, j, dir, k)

        if Pole._check(self) == 1:
            Pole.create(self)

    def _delo(self, i, j, dir, k):
        if dir == 'up' or dir == 'down':
            i1 = i
            j1 = j
            i += k
            while i >= 0 and i <= 3:
                if self.pole[i][j].pusto == 0:
                    if self.pole[i][j].chislo == self.pole[i1][j1].chislo:
                        self.pole[i][j].chislo *= 2
                        self.pole[i1][j1] = Kletka()
                        return
                    else:
                        break
                i += k
            self.pole[i - k][j].chislo = int(self.pole[i1][j1].chislo)
            if i1 != i - k:
                self.pole[i1][j1] = Kletka()
            self.pole[i - k][j].pusto = 0
            return

        else:
            i1 = i
            j1 = j
            j += k
            while j >= 0 and j <= 3:
                if self.pole[i][j].pusto == 0:
                    if self.pole[i][j].chislo == self.pole[i1][j1].chislo:
                        self.pole[i][j].chislo *= 2
                        self.pole[i1][j1] = Kletka()
                        return
                    else:
                        break
                j += k
            self.pole[i][j - k].chislo = int(self.pole[i1][j1].chislo)
            if j1 != j - k:
                self.pole[i1][j1] = Kletka()
            self.pole[i][j - k].pusto = 0
            return



    def create(self):
        x = []
        for i in range(4):
            for j in range(4):
                if self.pole[i][j].pusto == 1:
                    x.append([i, j])
        if len(x) > 0:
            x = random.choice(x)
            self.pole[x[0]][x[1]].pusto = 0
            if random.randrange(4) == 1:
                self.pole[x[0]][x[1]].chislo = 4

    def _check(self):
        global p
        for i in range(4):
            for j in range(4):
                if self.pole[i][j].pusto != p[i][j]:
                    return 1
        return 0




class Kletka:

    def __init__(self):
        self.pusto = 1
        self.chislo = 2

