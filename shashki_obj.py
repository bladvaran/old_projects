import pygame

h = 600
w = 600
k = 1

def mid(a, b):
    return (a + b) // 2

def change_hod(hod):
    if hod == 'p1':
        return 'p2'
    else:
        return 'p1'

def gener():
    pole = [[], [], [], [], [], [], [], [], [], []]
    for i in range(10):
        pole[0].append(Kletka(2, 0, 0))

    for i in range(1, 9):
        pole[i].append(Kletka(2, 0, 0))
        for j in range(1, 9):
            if i < 4:
                if i % 2 == j % 2:
                    pole[i].append(Kletka(0, 'Black', 'Black'))
                else:
                    pole[i].append(Kletka(1, 'White', 0))
            elif i > 5:
                if i % 2 == j % 2:
                    pole[i].append(Kletka(0, 'Black', 'White'))
                else:
                    pole[i].append(Kletka(1, 'White', 0))
            else:
                if i % 2 == j % 2:
                    pole[i].append(Kletka(1, 'Black', 0))
                else:
                    pole[i].append(Kletka(1, 'White', 0))
        pole[i].append(Kletka(2, 0, 0))

    for i in range(10):
        pole[9].append(Kletka(2, 0, 0))

    return pole


def doska_draw(screen, pole):

    pygame.draw.rect(screen, (200, 200, 200), (80, 80, 400, 400))
    x_rect = 30
    y_rect = 30
    for i in range(10):
        for j in range(10):
            if pole.pole[i][j].color == 'Black':
                pygame.draw.rect(screen, (100, 100, 100), (x_rect, y_rect, 50, 50))
            x_rect += 50
        x_rect = 30
        y_rect += 50
    pygame.draw.rect(screen, (200, 50, 50), (30 + pole.vibor['y'] * 50, 30 + pole.vibor['x'] * 50, 50, 50), 4)
    if pole.sost == 'vibrano':
        pygame.draw.rect(screen, (200, 100, 150), (30 + pole.vibrano['y'] * 50, 30 + pole.vibrano['x'] * 50, 50, 50), 4)
        if pole.pole[pole.vibrano['x'] - 1][pole.vibrano['y'] + 1].pusto == 1:
            pygame.draw.rect(screen, (200, 0, 0), (30 + pole.vibrano['y'] * 50 + 20 + 50, 30 + pole.vibrano['x'] * 50 + 20 - 50, 10, 10))
        if pole.pole[pole.vibrano['x'] - 1][pole.vibrano['y'] - 1].pusto == 1:
            pygame.draw.rect(screen, (200, 0, 0), (30 + pole.vibrano['y'] * 50 + 20 - 50, 30 + pole.vibrano['x'] * 50 + 20 - 50, 10, 10))
        if pole.bit != []:
            for i in range(len(pole.bit)):
                if pole.vibrano['x'] == pole.bit[i]['x'] and pole.vibrano['y'] == pole.bit[i]['y']:
                        pygame.draw.rect(screen, (0, 0, 0),(30 + (pole.bit[i]['y+'] + 1) * 50 + 20 - 50, 30 + (pole.bit[i]['x+'] + 1) * 50 + 20 - 50, 10, 10))

class Pole():

    def __init__(self):
        self.sost = 'vibor'
        self.vibrano = {'x': 0, 'y': 0}
        self.pole = gener()
        self.vibor = {'x': 0, 'y': 0}
        self.bit = []

    def update(self, key, key1):
        f = Pole.ubit(self)
        if key[pygame.K_w] and key1[pygame.K_w] == 0:
            self.vibor['x'] -= 1
        elif key[pygame.K_a] and key1[pygame.K_a] == 0:
            self.vibor['y'] -= 1
        elif key[pygame.K_d] and key1[pygame.K_d] == 0:
            self.vibor['y'] += 1
        elif key[pygame.K_s] and key1[pygame.K_s] == 0:
            self.vibor['x'] += 1
        elif (key[pygame.K_e]) and key1[pygame.K_e] == 0:
            print(self.pole[self.vibor['x']][self.vibor['y']].pusto)
            if self.sost == 'vibrano':
                if self.vibrano == self.vibor:
                    self.sost = 'vibor'
                elif (self.vibor['x'] == self.vibrano['x'] - 1 and self.vibor['y'] == self.vibrano['y'] - 1) or (self.vibor['x'] == self.vibrano['x'] - 1 and self.vibor['y'] == self.vibrano['y'] + 1):
                    self.pole[self.vibrano['x']][self.vibrano['y']], self.pole[self.vibor['x']][self.vibor['y']] = self.pole[self.vibor['x']][self.vibor['y']], self.pole[self.vibrano['x']][self.vibrano['y']]
                    self.sost = 'vibor'
                    pygame.time.wait(200)

                    Pole.perevorot(self)
                elif f != -1:
                    self.pole[self.bit[f]['x']][self.bit[f]['y']], self.pole[self.bit[f]['x+']][self.bit[f]['y+']] = self.pole[self.bit[f]['x+']][self.bit[f]['y+']], self.pole[self.bit[f]['x']][self.bit[f]['y']]
                    self.pole[mid(self.bit[f]['x'], self.bit[f]['x+'])][mid(self.bit[f]['y'], self.bit[f]['y+'])].pusto = 1
                    self.sost = 'vibor'
                    x = self.bit[f]
                    self.bit = []
                    Pole._prov(self, x['x+'], x['y+'], self.pole[x['x']][x['y']].shashka.color)
                    pygame.time.wait(200)
                    if self.bit == []:
                        Pole.perevorot(self)

            elif self.sost == 'vibor' and self.pole[self.vibor['x']][self.vibor['y']].pusto == 0:
                self.vibrano = dict(self.vibor)
                self.sost = 'vibrano'
        print(self.bit)
        Pole.proverka(self)

    def ubit(self):
        for i in range(len(self.bit)):
            if self.vibor['x'] == self.bit[i]['x+'] and self.vibor['y'] == self.bit[i]['y+']:
                return i
        return -1

    def kolvo_bit(self):
        k = 1
        for i in range(len(self.bit)):
            if self.pole[self.bit[i]['x']][self.bit[i]['y']].pusto == 1:
                k += 1
        return k

    def shaski_draw(self, screen):
        for i in range(1, 9):
            for j in range(1, 9):
                if self.pole[i][j].pusto == 0 and self.pole[i][j].shashka.color == 'Black':
                    pygame.draw.circle(screen, (0, 0, 0), (30 + j * 50 + 25, 30 + i * 50 + 25), 20)
                elif self.pole[i][j].pusto == 0 and self.pole[i][j].shashka.color == 'White':
                    pygame.draw.circle(screen, (255, 255, 255), (30 + j * 50 + 25, 30 + i * 50 + 25), 20)

    def perevorot(self):
        self.pole[1], self.pole[8] = self.pole[8], self.pole[1]
        self.pole[2], self.pole[7] = self.pole[7], self.pole[2]
        self.pole[3], self.pole[6] = self.pole[6], self.pole[3]
        self.pole[4], self.pole[5] = self.pole[5], self.pole[4]
        for i in range(1, 9):
            self.pole[i].reverse()
        self.vibor['y'] = 8 - self.vibor['y']

    def proverka(self):
        self.bit = []
        for i in range(1, 9):
            for j in range(1, 9):
                if self.pole[i][j].pusto == 0:
                    Pole._prov(self, i, j, self.pole[i][j].shashka.color)


    def _prov(self, x, y, cl):
        l = 0
        if self.pole[x + 1][y + 1].pusto == 0 and self.pole[x + 2][y + 2].pusto == 1:
            if self.pole[x + 1][y + 1].shashka.color != cl:
                self.bit.append({'x': x, 'y': y, 'x+': x + 2, 'y+': y + 2})
                l, self.pole[x][y].pusto = self.pole[x][y].pusto, 0
                Pole._prov(self, x + 2, y + 2, cl)
                self.pole[x][y].pusto = l


        if self.pole[x - 1][y + 1].pusto == 0 and self.pole[x - 2][y + 2].pusto == 1:
            if self.pole[x - 1][y + 1].shashka.color != cl:
                self.bit.append({'x': x, 'y': y, 'x+': x - 2, 'y+': y + 2})
                l, self.pole[x][y].pusto = self.pole[x][y].pusto, 0
                Pole._prov(self, x - 2, y + 2, cl)
                self.pole[x][y].pusto = l

        if self.pole[x + 1][y - 1].pusto == 0 and self.pole[x + 2][y - 2].pusto == 1:
            if self.pole[x + 1][y - 1].shashka.color != cl:
                self.bit.append({'x': x, 'y': y, 'x+': x + 2, 'y+': y - 2})
                l, self.pole[x][y].pusto = self.pole[x][y].pusto, 0
                Pole._prov(self, x + 2, y - 2, cl)
                self.pole[x][y].pusto = l

        if self.pole[x - 1][y - 1].pusto == 0 and self.pole[x - 2][y - 2].pusto == 1:
            if self.pole[x - 1][y - 1].shashka.color != cl:
                self.bit.append({'x': x, 'y': y, 'x+': x - 2, 'y+': y - 2})
                l, self.pole[x][y].pusto = self.pole[x][y].pusto, 0
                Pole._prov(self, x - 2, y - 2, cl)
                self.pole[x][y].pusto = l

class Shashka():

    def __init__(self, color):
        self.color = color

class Kletka():

    def __init__(self, pusto, color, color_shashki):
        self.pusto = pusto
        self.color = color
        self.shashka = Shashka(color_shashki)