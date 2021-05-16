import pygame
import random

pygame.init()
w = 480
h = 640

def add():
    r = random.randrange(5)
    if r == 0:
        return Palka()
    elif r == 1:
        return Kvadrat()
    elif r == 2:
        return Molnia_1()
    elif r == 3:
        return Molnia_2()
    elif r == 4:
        return Tank()

class Figure():

    def __init__(self):
        self.rect = [{'x': random.choice([int(i) for i in range(60, 421) if i % 20 == 0]), 'y': -20}]
        self.status = random.randrange(2)
        self.rect.append({'x': self.rect[0]['x'], 'y': self.rect[0]['y']})
        self.rect.append({'x': self.rect[0]['x'], 'y': self.rect[0]['y']})
        self.rect.append({'x': self.rect[0]['x'], 'y': self.rect[0]['y']})

    def update(self, key, figure):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_UP]) and (key[pygame.K_UP] == 0):
            figure.change_status(self.status)
        if keys[pygame.K_RIGHT] and (key[pygame.K_RIGHT] == 0):
            self.rect[0]['x'] += 20
        elif keys[pygame.K_LEFT] and (key[pygame.K_LEFT] == 0):
            self.rect[0]['x'] -= 20


    def change_status(self, status):
        if status == 1:
            self.status = 0
        else:
            self.status = 1

class Palka(Figure):

    def __init__(self):
        Figure.__init__(self)

    def update(self, key, figure):
        Figure.update(self, key, figure)
        if self.status == 1:
            self.rect[1]['y'] = self.rect[0]['y'] - 20
            self.rect[2]['y'] = self.rect[0]['y'] - 40
            self.rect[3]['y'] = self.rect[0]['y'] - 60

            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = int(self.rect[0]['x'])
            self.rect[3]['x'] = int(self.rect[0]['x'])
        elif self.status == 0:
            self.rect[1]['x'] = self.rect[0]['x'] + 20
            self.rect[2]['x'] = self.rect[0]['x'] + 40
            self.rect[3]['x'] = self.rect[0]['x'] + 60

            self.rect[1]['y'] = int(self.rect[0]['y'])
            self.rect[2]['y'] = int(self.rect[0]['y'])
            self.rect[3]['y'] = int(self.rect[0]['y'])

class Kvadrat(Figure):

    def __init__(self):
        Figure.__init__(self)

    def update(self, key, figure):
        Figure.update(self, key, figure)
        if (self.status == 1) or (self.status == 0):
            self.rect[1]['y'] = int(self.rect[0]['y'])
            self.rect[2]['y'] = self.rect[0]['y'] - 20
            self.rect[3]['y'] = self.rect[0]['y'] - 20

            self.rect[1]['x'] = self.rect[0]['x'] + 20
            self.rect[2]['x'] = int(self.rect[0]['x'])
            self.rect[3]['x'] = self.rect[0]['x'] + 20

class Molnia_1(Figure):

    def __init__(self):
        Figure.__init__(self)

    def update(self, key, figure):
        Figure.update(self, key, figure)
        if self.status == 1:
            self.rect[1]['y'] = int(self.rect[0]['y'])
            self.rect[2]['y'] = self.rect[0]['y'] - 20
            self.rect[3]['y'] = self.rect[0]['y'] - 20

            self.rect[1]['x'] = int(self.rect[0]['x']) + 20
            self.rect[2]['x'] = int(self.rect[0]['x']) + 20
            self.rect[3]['x'] = int(self.rect[0]['x']) + 40
        elif self.status == 0:
            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = self.rect[0]['x'] - 20
            self.rect[3]['x'] = self.rect[0]['x'] - 20

            self.rect[1]['y'] = int(self.rect[0]['y']) - 20
            self.rect[2]['y'] = int(self.rect[0]['y']) - 20
            self.rect[3]['y'] = int(self.rect[0]['y']) - 40

class Molnia_2(Figure):

    def __init__(self):
        Figure.__init__(self)

    def update(self, key, figure):
        Figure.update(self, key, figure)
        if self.status == 1:
            self.rect[1]['y'] = int(self.rect[0]['y'])
            self.rect[2]['y'] = self.rect[0]['y'] - 20
            self.rect[3]['y'] = self.rect[0]['y'] - 20

            self.rect[1]['x'] = int(self.rect[0]['x']) - 20
            self.rect[2]['x'] = int(self.rect[0]['x']) - 20
            self.rect[3]['x'] = int(self.rect[0]['x']) - 40
        elif self.status == 0:
            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = self.rect[0]['x'] + 20
            self.rect[3]['x'] = self.rect[0]['x'] + 20

            self.rect[1]['y'] = int(self.rect[0]['y']) - 20
            self.rect[2]['y'] = int(self.rect[0]['y']) - 20
            self.rect[3]['y'] = int(self.rect[0]['y']) - 40

class Tank(Figure):

    def __init__(self):
        Figure.__init__(self)

    def update(self, key, figure):
        Figure.update(self, key, figure)
        if self.status == 0:
            self.rect[1]['y'] = int(self.rect[0]['y']) - 20
            self.rect[2]['y'] = int(self.rect[0]['y'])
            self.rect[3]['y'] = int(self.rect[0]['y'])

            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = int(self.rect[0]['x']) - 20
            self.rect[3]['x'] = int(self.rect[0]['x']) + 20
        elif self.status == 1:
            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = self.rect[0]['x'] + 20
            self.rect[3]['x'] = int(self.rect[0]['x'])

            self.rect[1]['y'] = int(self.rect[0]['y']) - 20
            self.rect[2]['y'] = int(self.rect[0]['y'])
            self.rect[3]['y'] = int(self.rect[0]['y']) + 20
        elif self.status == 2:
            self.rect[1]['y'] = int(self.rect[0]['y'])
            self.rect[2]['y'] = int(self.rect[0]['y'])
            self.rect[3]['y'] = self.rect[0]['y'] + 20

            self.rect[1]['x'] = int(self.rect[0]['x']) - 20
            self.rect[2]['x'] = int(self.rect[0]['x']) + 20
            self.rect[3]['x'] = int(self.rect[0]['x'])
        elif self.status == 3:
            self.rect[1]['x'] = int(self.rect[0]['x'])
            self.rect[2]['x'] = self.rect[0]['x'] - 20
            self.rect[3]['x'] = int(self.rect[0]['x'])

            self.rect[1]['y'] = int(self.rect[0]['y']) - 20
            self.rect[2]['y'] = int(self.rect[0]['y'])
            self.rect[3]['y'] = int(self.rect[0]['y']) + 20

    def change_status(self, status):
        if status != 3:
            self.status += 1
        else:
            self.status = 0

class Pole():

    def __init__(self):
        self.kvadratiki = []

    def printer(self, screen):
        for i in range(len(self.kvadratiki)):
            pygame.draw.rect(screen, (255, 250, 250), (self.kvadratiki[i]['x'] - 10, self.kvadratiki[i]['y'] - 10, 21, 21), 3)
            pygame.draw.rect(screen, (255, 250, 250), (self.kvadratiki[i]['x'] - 5, self.kvadratiki[i]['y'] - 5, 10, 10))

    def update(self, figure):
        for j in range(4):
            for i in range(len(self.kvadratiki)):
                if (figure.rect[j]['x'] == self.kvadratiki[i]['x']) and (self.kvadratiki[i]['y'] - figure.rect[j]['y'] == 20):
                    return 1


    def prov(self, screen):
        y = 0
        while y <= 580:
            i = 60
            f = 0
            while i <= 420:
                if screen.get_at((i, y))[0] != 255:
                    f = 1
                    break
                i += 20
            if f == 0:
                Pole._udalenie(self, y)
            y += 20

    def _udalenie(self, y):
        for i in range(len(self.kvadratiki)):
            if self.kvadratiki[i]['y'] == y:
                self.kvadratiki[i] = 0
            elif self.kvadratiki[i]['y'] < y:
                self.kvadratiki[i]['y'] += 20
        self.kvadratiki = [self.kvadratiki[i] for i in range(len(self.kvadratiki)) if self.kvadratiki[i] != 0]