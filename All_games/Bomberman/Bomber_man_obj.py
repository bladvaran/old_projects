import pygame as pg
from random import *
from pygame.locals import *
from collections import deque

pg.init()
pg.font.init()

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

FETIL_COLORS = [(255, 0, 0), (128, 0, 0), (255, 69, 0), (255, 140, 0), (255, 255, 0)]


size_of_cell = 30


class Player:

    def __init__(self, x, y, up, down, left, right, bomb_key):
        self.position = pg.math.Vector2()
        self.position.x = x
        self.position.y = y
        self.r = 10
        self.color = (randrange(256), randrange(256), randrange(256))
        self.color_buf = self.color
        self.timer = 0
        self.text_event = ''
        self.text_timer = 0
        self.event = ''
        self.obodok = 1

        self.font = pg.font.SysFont('comicsansms', 15)
        self.font.set_bold(4)
        self.text = None

        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.bomb_key = bomb_key

        self.bomb_kol = 1
        self.bomb_power = 1

        self.speed = 1

    def update(self, keys, a, players):
        j, i = get_index(self.position.x, self.position.y)

        if type(a[i][j]) == Boom or type(a[i][j]) == Bomb:
            if type(a[i][j]) == Bomb:
                if not a[i][j].Boom:
                    pass
                else:
                    players.remove(self)
                    return
            else:
                players.remove(self)

        if self.event == 'BOMBS':
            if pg.time.get_ticks() - self.timer > 4401:
                self.event = ''
                self.timer = 0
                self.color = self.color_buf
            else:
                if pg.time.get_ticks() - self.timer < 2400:
                    if type(a[i][j]) != Bomb:
                        a[i][j] = Bomb(self, i, j, pg.time.get_ticks())
                self.color = WHITE if randrange(2) == 1 else BLACK
        elif self.event == '*':
            if pg.time.get_ticks() - self.timer > 5000:
                self.event = ''
                self.timer = 0
                self.up, self.down = self.down, self.up
                self.left, self.right = self.right, self.left
                self.color = self.color_buf
            else:
                if (pg.time.get_ticks() - self.timer) % 7 == 0:
                    self.color = (randrange(256), randrange(256), randrange(256))
        elif self.text_event == 'speed' or self.text_event == 'bomb' or self.text_event == 'power':
            if pg.time.get_ticks() - self.text_timer > 2000:
                self.text_event = ''
                self.text_timer = 0
        elif self.event == 'shok':
            if pg.time.get_ticks() - self.text_timer > 5000:
                self.event = ''
                self.timer = 0
                do_cell(a, i, j, 0)
                do_cell(a, i + 1, j, 0)
                do_cell(a, i, j + 1, 0)
                do_cell(a, i - 1, j, 0)
                do_cell(a, i, j - 1, 0)

        if a[i][j] == 7:
            chance = randrange(11)

            self.text_timer = pg.time.get_ticks()
            self.timer = pg.time.get_ticks()

            if self.event == '*':
                self.event = ''
                self.timer = 0
                self.up, self.down = self.down, self.up
                self.left, self.right = self.right, self.left
                self.color = self.color_buf

            if chance == 1:
                self.speed += 0.4
                self.text_event = 'speed'
                self.text = self.font.render('SPEED +1', False, RED)
            elif chance == 2:
                self.bomb_kol += 1
                self.text_event = 'bomb'
                self.text = self.font.render('BOMB +1', False, RED)
            elif chance == 0:
                self.bomb_power += 1
                self.text_event = 'power'
                self.text = self.font.render('POWER +1', False, RED)
            elif chance == 3:
                if 0 <= randrange(101) <= 5:
                    self.color = GREEN
                    self.obodok = 0
                else:
                    self.color = (randrange(256), randrange(256), randrange(256))
                    self.obodok = 1
            elif chance == 4:
                self.position.x = randrange(256)
                self.position.y = randrange(256)
                j1, i1 = get_index(self.position.x, self.position.y)
                do_cell(a, i1, j1, 0)
                do_cell(a, i1 + 1, j1, 0)
                do_cell(a, i1, j1 + 1, 0)
                do_cell(a, i1 - 1, j1, 0)
                do_cell(a, i1, j1 - 1, 0)
            elif chance == 5:
                self.event = 'BOMBS'
                self.color_buf = self.color
            elif chance == 6:
                self.color_buf = self.color
                if self.event != '*':
                    self.up, self.down = self.down, self.up
                    self.left, self.right = self.right, self.left
                self.event = '*'
                self.color = (randrange(256), randrange(256), randrange(256))
            elif chance == 7:
                if len(players) == 1:
                    return
                player = choice(players)
                while player == self:
                    player = choice(players)
                player.bomb_key, self.bomb_key = self.bomb_key, player.bomb_key
                player.up, self.up = self.up, player.up
                player.down, self.down = self.down, player.down
                player.left, self.left = self.left, player.left
                player.right, self.right = self.right, player.right
            elif chance == 8:
                self.event = 'shok'
            elif chance == 9:
                a[randrange(20)][randrange(20)] = 7
            elif chance == 10:
                for i1 in range(7, 14):
                    for j1 in range(7, 14):
                        if i1 == 7 or i1 == 13 or j1 == 7 or j1 == 13:
                            do_cell(a, i1, j1, 1)
                        else:
                            do_cell(a, i1, j1, 0)
                for player in players:
                    player.position.x = 315
                    player.position.y = 315
            a[i][j] = 0

        if keys[self.up]:
            if a[i - 1][j] != 0 and type(a[i - 1][j]) != Boom and a[i - 1][j] != 7 and self.event != 'shok':
                if i * size_of_cell + self.r < self.position.y:
                    self.position.y -= self.speed
            else:
                self.position.y -= self.speed

        if keys[self.down]:
            if a[i + 1][j] != 0 and type(a[i + 1][j]) != Boom and a[i + 1][j] != 7 and self.event != 'shok':
                if (i + 1) * size_of_cell - self.r > self.position.y:
                    self.position.y += self.speed
            else:
                self.position.y += self.speed

        if keys[self.right]:
            if a[i][j + 1] != 0 and type(a[i][j + 1]) != Boom and a[i][j + 1] != 7 and self.event != 'shok':
                if (j + 1) * size_of_cell - self.r > self.position.x:
                    self.position.x += self.speed
            else:
                self.position.x += self.speed

        if keys[self.left]:
            if a[i][j - 1] != 0 and type(a[i][j - 1]) != Boom and a[i][j - 1] != 7 and self.event != 'shok':
                if j * size_of_cell + self.r < self.position.x:
                    self.position.x -= self.speed
            else:
                self.position.x -= self.speed

        if keys[self.bomb_key]:
            if type(a[i][j]) != Bomb and self.bomb_kol > 0 and self.event != 'BOMBS':
                self.bomb_kol -= 1
                a[i][j] = Bomb(self, i, j, pg.time.get_ticks())


class Boom:

    def __init__(self, i, j, time, type):
        self.i = i
        self.j = j
        self.start_time = time
        self.history = deque([])
        self.type = type
        self.center_type = None


class Bomb:

    def __init__(self, player, i, j, time):
        self.power = player.bomb_power
        self.player = player
        self.start_time = time
        self.Boom = None
        self.i = i
        self.j = j

    def boom(self, a):
        now_time = pg.time.get_ticks()
        self.boom_dir(a, 1, 0, now_time)
        self.boom_dir(a, 0, 1, now_time)
        self.boom_dir(a, 0, -1, now_time)
        self.boom_dir(a, -1, 0, now_time)
        a[self.i][self.j] = Boom(self.i, self.j, pg.time.get_ticks(), 'center')
        a[self.i][self.j].center_type = 1
        if self.player.event != 'BOMBS':
            self.player.bomb_kol += 1

    def boom_dir(self, a, delta_i, delta_j, now_time):
        i = self.i
        j = self.j

        while self.i - self.power <= i <= self.i + self.power and self.j - self.power <= j <= self.j + self.power:
            if a[i][j] == 2:
                break

            if type(a[i][j]) == Boom:
                a[i][j].history.append(['vertical' if delta_i != 0 else 'horizontal', pg.time.get_ticks()])
            else:
                if a[i][j] == 1:
                    if 0 <= randrange(101) <= 15:
                        a[i][j] = 7
                    else:
                        a[i][j] = Boom(i, j, now_time, 'vertical' if delta_i != 0 else 'horizontal')
                    break
                else:
                    if type(a[i][j]) != Bomb:
                        a[i][j] = Boom(i, j, now_time, 'vertical' if delta_i != 0 else 'horizontal')

            i += delta_i
            j += delta_j
            if type(a[i][j]) == Bomb:
                a[i][j].Boom = Boom(i, j, now_time, 'vertical' if delta_i != 0 else 'horizontal')

    def draw_fetil(self, screen):
        k = (2000 - pg.time.get_ticks() + self.start_time) / 2000
        if 10 * k > 1:
            pg.draw.rect(screen, WHITE, (self.j * size_of_cell + 10, self.i * size_of_cell + 13, max(10 * k, 1), 4))


class Drawer:

    def draw_wall_break(self, screen, x, y):
        pg.draw.rect(screen, BLACK, (size_of_cell * x, size_of_cell * y, size_of_cell, size_of_cell), 2)
        pg.draw.rect(screen, SILVER, (size_of_cell * x + 3, size_of_cell * y + 3, size_of_cell - 6, size_of_cell - 6))

    def draw_wall_UNbreak(self, screen, x, y):
        pg.draw.rect(screen, BLACK, (size_of_cell * x, size_of_cell * y, size_of_cell, size_of_cell), 2)
        pg.draw.rect(screen, WHITE, (size_of_cell * x + 3, size_of_cell * y + 3, size_of_cell - 6, size_of_cell - 6))

    def draw_cell(self, screen, x, y):
        pg.draw.rect(screen, GREEN, (size_of_cell * x, size_of_cell * y, size_of_cell, size_of_cell))

    def draw_a(self, screen, a):
        for i in range(len(a)):
            for j in range(len(a)):
                if a[i][j] == 0:
                    Drawer.draw_cell(self, screen, j, i)
                elif a[i][j] == 1:
                    Drawer.draw_wall_break(self, screen, j, i)
                elif a[i][j] == 2:
                    Drawer.draw_wall_UNbreak(self, screen, j, i)
                elif type(a[i][j]) == Boom or type(a[i][j]) == Bomb:
                    if type(a[i][j]) == Bomb:

                        if a[i][j].Boom:
                            if a[i][j].Boom.type == 'horizontal':
                                Drawer.draw_cell(self, screen, j, i)
                                pg.draw.rect(screen, ORANGE, (j * size_of_cell, i * size_of_cell + 5, size_of_cell, 20))
                                pg.draw.rect(screen, YELLOW, (j * size_of_cell, i * size_of_cell + 10, size_of_cell, 10))
                            elif a[i][j].Boom.type == 'vertical':
                                Drawer.draw_cell(self, screen, j, i)
                                pg.draw.rect(screen, ORANGE, (j * size_of_cell + 5, i * size_of_cell, 20, size_of_cell))
                                pg.draw.rect(screen, YELLOW, (j * size_of_cell + 10, i * size_of_cell, 10, size_of_cell))
                            elif a[i][j].Boom.type == 'center':
                                Drawer.draw_cell(self, screen, j, i)
                                pg.draw.rect(screen, ORANGE, (j * size_of_cell, i * size_of_cell + 5, size_of_cell, 20))
                                pg.draw.rect(screen, ORANGE, (j * size_of_cell + 5, i * size_of_cell, 20, size_of_cell))
                                pg.draw.rect(screen, YELLOW, (j * size_of_cell, i * size_of_cell + 10, size_of_cell, 10))
                                pg.draw.rect(screen, YELLOW, (j * size_of_cell + 10, i * size_of_cell, 10, size_of_cell))
                                if a[i][j].Boom.center_type == 1:
                                    pg.draw.rect(screen, BRIGHT_RED, (j * size_of_cell + 3, i * size_of_cell + 3, 24, 24))
                    else:
                        if a[i][j].type == 'horizontal':
                            Drawer.draw_cell(self, screen, j, i)
                            pg.draw.rect(screen, ORANGE, (j * size_of_cell, i * size_of_cell + 5, size_of_cell, 20))
                            pg.draw.rect(screen, YELLOW, (j * size_of_cell, i * size_of_cell + 10, size_of_cell, 10))
                        elif a[i][j].type == 'vertical':
                            Drawer.draw_cell(self, screen, j, i)
                            pg.draw.rect(screen, ORANGE, (j * size_of_cell + 5, i * size_of_cell, 20, size_of_cell))
                            pg.draw.rect(screen, YELLOW, (j * size_of_cell + 10, i * size_of_cell, 10,  size_of_cell))
                        elif a[i][j].type == 'center' or a[i][j].boom.type == 'center':
                            Drawer.draw_cell(self, screen, j, i)
                            pg.draw.rect(screen, ORANGE, (j * size_of_cell, i * size_of_cell + 5, size_of_cell, 20))
                            pg.draw.rect(screen, ORANGE, (j * size_of_cell + 5, i * size_of_cell, 20, size_of_cell))
                            pg.draw.rect(screen, YELLOW, (j * size_of_cell, i * size_of_cell + 10, size_of_cell, 10))
                            pg.draw.rect(screen, YELLOW, (j * size_of_cell + 10, i * size_of_cell, 10, size_of_cell))
                            if a[i][j].center_type == 1:
                                pg.draw.rect(screen, BRIGHT_RED, (j * size_of_cell + 3, i * size_of_cell + 3, 24, 24))
                if type(a[i][j]) == Bomb:
                    if not a[i][j].Boom:
                        Drawer.draw_cell(self, screen, j, i)
                    if pg.time.get_ticks() - a[i][j].start_time > 2000:
                        pg.draw.circle(screen, BLACK, (j * size_of_cell + 15, i * size_of_cell + 15), 14)
                        pg.draw.rect(screen, GRAY, (j * size_of_cell + 8, i * size_of_cell + 11, 14, 8))
                    else:
                        pg.draw.circle(screen, BLACK, (j * size_of_cell + 15, i * size_of_cell + 15), 9)
                        pg.draw.rect(screen, GRAY, (j * size_of_cell + 10, i * size_of_cell + 13, 10, 4))
                        a[i][j].draw_fetil(screen)
                elif a[i][j] == 7:
                    Drawer.draw_cell(self, screen, j, i)
                    pg.draw.rect(screen, RED, (j * size_of_cell + 7, i * size_of_cell + 7, 16, 16))
                    pg.draw.circle(screen, WHITE, (j * size_of_cell + 15, i * size_of_cell + 15), 3)

    def draw_player(self, screen, player):
        if player.event == 'shok':
            pg.draw.circle(screen, BLACK, (int(player.position.x), int(player.position.y)), player.r + 1, 1)
            return
        if player.obodok:
            pg.draw.circle(screen, BLACK, (int(player.position.x), int(player.position.y)), player.r + 1)
        if player.event != 'shok':
            pg.draw.circle(screen, player.color, (int(player.position.x), int(player.position.y)), player.r)

        if player.text_event == 'speed' or player.text_event == 'bomb' or player.text_event == 'power':
            screen.blit(player.text, (player.position.x - 25, player.position.y - 25))


def get_index(x, y):
    return [int(x) // size_of_cell, int(y) // size_of_cell]


# Контроль таймингов
def update_a(a):

    for i in range(20):
        for j in range(20):
            if type(a[i][j]) == Bomb:
                if pg.time.get_ticks() - a[i][j].start_time > 2000:
                    a[i][j].boom(a)
                    pass
            elif type(a[i][j]) == Boom:
                if pg.time.get_ticks() - a[i][j].start_time > 1000:
                    if a[i][j].history:
                        a[i][j].type, a[i][j].start_time = a[i][j].history.popleft()
                        if find_his(a[i][j]):
                            a[i][j].type = 'center'
                            if not a[i][j].center_type:
                                a[i][j].center_type = 0
                    else:
                        a[i][j] = 0
                else:
                    if find_his(a[i][j]):
                        a[i][j].type = 'center'
                        if not a[i][j].center_type:
                            a[i][j].center_type = 0


def find_his(boom):
    for i in range(len(boom.history)):
        if boom.history[i][0] != boom.type:
            return 1
    return 0


def do_cell(a, i, j, cell):
    if type(a[i][j]) == Bomb:
        a[i][j].player.bomb_kol += 1
    a[i][j] = cell
