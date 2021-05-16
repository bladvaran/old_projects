import pygame as pg
from pygame.math import Vector2
import os
from pygame.locals import *
from random import *
from Tenis_menu import *
from time import *

pg.init()
size = (700, 700)

os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (size[0] // 2, 26)

MIN_spin_angle = 6
MAX_spin_angle = 15

MIN_spin_frames = 20
MAX_spin_frames = 80

MIN_spin_pick = 0
MAX_spin_pick = 1

screen = pg.display.set_mode(size)
clock = pg.time.Clock()

platform_size = (120, 12)
platform_distance = 50
frames_to_start_move = 5
frames_to_finish_move = 5
platform_speed = 10
ball_speed = 12
ball_size = 20

vorota_size = (500, 20)
vorota_otstup = (size[0] - vorota_size[0]) / 2

font_size = 60
score_font = pg.font.SysFont('comicsansms', font_size)


class Spin:
    def __init__(self):
        self.angle = 0
        self.max_angle = 0
        self.frames = 0
        self.start_frames = 0
        self.direction = 0

        self.max_spin_angle = 10
        self.max_spin_frames = 20
        self.spin_pick = self.max_spin_frames / 2

    def update(self, ball):
        if self.frames <= self.spin_pick:
            a = -self.max_angle / (self.spin_pick * self.spin_pick)
            self.angle = a * self.frames * (self.frames - 2 * self.spin_pick) / self.max_spin_frames * self.max_angle
        elif self.frames <= self.max_spin_frames:
            k = -self.max_angle / (self.max_spin_frames - self.spin_pick)
            b = -k * self.max_spin_frames
            self.angle = (k * self.frames + b) / self.max_spin_frames * self.max_angle
        else:
            self.angle = 0
        self.frames += 1
        ball.v.rotate_ip(self.direction * self.angle)


class Wall:
    def __init__(self, rect, kuda):
        self.rect = rect
        self.kuda = kuda


def change_dir(v, wall_dir):
    if wall_dir == 'right':
        return Vector2(v.x, -v.y)
    else:
        return Vector2(-v.x, v.y)


def po_or_protiv(ball, platform):
    if platform.x > 0:
        if ball.y > 0:
            return -1
        else:
            return 1
    elif platform.x < 0:
        if ball.y > 0:
            return 1
        else:
            return -1
    elif platform.y > 0:
        if ball.x > 0:
            return 1
        else:
            return -1
    elif platform.y < 0:
        if ball.x > 0:
            return -1
        else:
            return 1
    else:
        return 0


class Platform:
    def __init__(self, menu):
        self.num = menu.num
        kuda = 'right' if menu.num % 2 != 0 else 'up'
        x = menu.x
        y = menu.y

        if menu.num == 1:
            y -= 100
        elif menu.num == 2:
            x += 100
        elif menu.num == 3:
            y += 100
        elif menu.num == 4:
            x -= 100

        if kuda == 'right':
            self.rect = Rect(x - platform_size[0] // 2, y - platform_size[1] // 2, platform_size[0], platform_size[1])
            self.pos = Vector2(x - platform_size[0] // 2, y - platform_size[1] // 2)
        else:
            self.rect = Rect(x - platform_size[1] // 2, y - platform_size[0] // 2, platform_size[1], platform_size[0])
            self.pos = Vector2(x - platform_size[1] // 2, y - platform_size[0] // 2)
        self.v = None
        self.kuda = kuda
        self.in_move = 0
        self.not_in_move = 0
        self.speed_now = Vector2(0, 0)

        self.max_spin_angle = MIN_spin_angle + (MAX_spin_angle - MIN_spin_angle) / 5 * menu.changer1.level
        self.max_spin_frames = MIN_spin_frames + (MAX_spin_frames - MIN_spin_frames) / 5 * menu.changer2.level
        self.spin_pick = self.max_spin_frames * (MAX_spin_pick - MIN_spin_pick) / 5 * menu.changer3.level

        self.up_key = menu.up_key
        self.left_key = menu.left_key
        self.down_key = menu.down_key
        self.right_key = menu.right_key

    def update(self, key, key0):
        self.movement(key, key0)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def draw(self, screen):
        pg.draw.rect(screen, (255, 255, 255), self.rect)

    def movement(self, key, key0):

        if key[self.up_key] and not key0[self.down_key] and self.kuda == 'up':
            self.v = Vector2(0, -1)
            self.in_move += 1
            self.not_in_move = 0
        elif key[self.down_key] and not key0[self.up_key] and self.kuda == 'up':
            self.v = Vector2(0, 1)
            self.in_move += 1
            self.not_in_move = 0
        elif key[self.left_key] and not key0[self.right_key] and self.kuda == 'right':
            self.v = Vector2(-1, 0)
            self.in_move += 1
            self.not_in_move = 0
        elif key[self.right_key] and not key0[self.left_key] and self.kuda == 'right':
            self.v = Vector2(1, 0)
            self.in_move += 1
            self.not_in_move = 0
        else:
            self.not_in_move += 1
            self.in_move = 0

        if not self.v:
            return

        if 0 < self.in_move <= frames_to_start_move:
            self.speed_now = self.v * (platform_speed / frames_to_start_move * self.in_move)
            self.pos += self.speed_now
        elif self.in_move:
            self.speed_now = self.v * platform_speed
            self.pos += self.speed_now
        elif 0 < self.not_in_move <= frames_to_finish_move:
            self.speed_now = self.v * (platform_speed / frames_to_finish_move * max(frames_to_finish_move - self.not_in_move, 0))
            self.pos += self.speed_now
        else:
            self.speed_now = Vector2(0, 0)


class Ball:
    def __init__(self):
        self.v = Vector2(random() - 0.5, random() - 0.5).normalize()
        self.rect = Rect(size[0] / 2, size[1] / 2, ball_size, ball_size)
        self.spin = Spin()
        self.pos = Vector2(self.rect.centerx, self.rect.centery)
        self.speed = ball_speed

    def draw(self, screen):
        pg.draw.rect(screen, (200, 0, 0), self.rect)

    def update(self, platforms, vorota):
        self.spin.update(self)
        new_pos = self.check_collide(self.pos + self.v * self.speed, platforms, vorota)
        self.pos = new_pos
        if not pg.display.get_surface().get_rect().collidepoint(self.pos):
            self.pos = Vector2(size[0] // 2, size[1] // 2)
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def gol(self, platform):
        if platform.num == 1:
            if self.v.y > 0:
                return 1
            else:
                return 0
        elif platform.num == 2:
            if self.v.x < 0:
                return 1
            else:
                return 0
        elif platform.num == 3:
            if self.v.y < 0:
                return 1
            else:
                return 0
        elif platform.num == 4:
            if self.v.x > 0:
                return 1
            else:
                return 0

    def check_collide(self, pos, platforms, vorota):
        min_part = (pos - self.pos).normalize()
        for i in range(self.speed):
            now_part = min_part * i
            new_rect = self.rect.copy()
            new_rect.center = (self.pos.x + now_part.x, self.pos.y + now_part.y)
            for platform in platforms:
                if platform.rect.colliderect(new_rect):
                    if type(platform) == Platform:
                        if self.gol(platform):
                            continue

                        self.spin.max_spin_angle = platform.max_spin_angle
                        self.spin.max_spin_frames = platform.max_spin_frames
                        self.spin.spin_pick = platform.spin_pick

                        self.spin.max_angle = (platform.speed_now.x or platform.speed_now.y) / platform_speed * platform.max_spin_angle
                        self.spin.frames = 0
                        self.spin.start_frames = self.spin.frames
                        self.spin.direction = po_or_protiv(min_part, platform.speed_now)
                    new_v = change_dir(pos - self.pos - now_part, platform.kuda)

                    self.v = new_v.normalize()
                    new_rect.center = ((self.pos + (now_part + new_v)).x, (self.pos + (now_part + new_v)).y)
                    while platform.rect.colliderect(new_rect):
                        new_v += self.v
                        new_rect.center = ((self.pos + (now_part + new_v)).x, (self.pos + (now_part + new_v)).y)

                    return self.pos + (now_part + new_v)

            for vorot in vorota:
                if vorot.rect.colliderect(new_rect):
                    if not vorot.inside:
                        vorot.inside = 1
                        vorot.score += 1
                else:
                    if vorot.inside:
                        vorot.inside = 0

        return pos


class Vorota:
    def __init__(self, num):
        self.score = 0
        self.inside = 0
        self.surface = pg.Surface((vorota_size[0], vorota_size[1]) if num == 1 or num == 3 else (vorota_size[1], vorota_size[0]))
        if num == 1:
            self.rect = Rect(vorota_otstup, 0, vorota_size[0], vorota_size[1])
            self.text_pos = (size[0] // 2 - font_size // 2, size[1] // 2 - 3 * font_size // 2)
        elif num == 2:
            self.rect = Rect(size[0] - vorota_size[1], vorota_otstup, vorota_size[1], vorota_size[0])
            self.text_pos = (size[0] // 2 + font_size // 2, size[1] // 2 - font_size // 2)
        elif num == 3:
            self.rect = Rect(vorota_otstup, size[1] - vorota_size[1], vorota_size[0], vorota_size[1])
            self.text_pos = (size[0] // 2 - font_size // 2, size[1] // 2 + font_size // 2)
        elif num == 4:
            self.rect = Rect(0, vorota_otstup, vorota_size[1], vorota_size[0])
            self.text_pos = (size[0] // 2 - 3 * font_size // 2, size[1] // 2 - font_size // 2)

    def draw(self, screen):
        self.surface.fill((255, 255, 255))
        self.surface.set_alpha(50)
        screen.blit(self.surface, (self.rect.x, self.rect.y))

        text_surface = score_font.render(str(self.score), False, (255, 255, 255))
        text_surface.set_alpha(100)
        screen.blit(text_surface, self.text_pos)



platforms = []
vorota = []

finish = 0
start = 1
XY = -15
walls = [Wall(Rect(XY, XY, size[0], 20), 'right'),
         Wall(Rect(XY, size[1], size[0], 20), 'right'),
         Wall(Rect(XY, XY, 20, size[1]), 'up'),
         Wall(Rect(size[0], XY, 20, size[1]), 'up')]
ball = Ball()
key0 = pg.key.get_pressed()

print('''1. Угол закрутки
2. Длительность закрутки
3. Пик закрутки''')

type_screen = 'menu'
menus = [Menu((size[0] // 2, 150), K_w, K_a, K_s, K_d, 1),
         Menu((size[0] - 150, size[1] // 2), K_y, K_g, K_h, K_j, 2),
         Menu((size[0] // 2, size[1] - 150), K_p, K_l, K_SEMICOLON, K_QUOTE, 3),
         Menu((150, size[1] // 2), K_KP8, K_KP4, K_KP5, K_KP6, 4)]

while 1:

    for event in pg.event.get():
        if event.type == QUIT:
            exit(0)

    if finish == 1:
        platforms = []
        vorota = []
        ball = Ball()
        type_screen = 'menu'
        for menu in menus:
            if menu.active == 'button_ok':
                menu.menu_status = 1
                menu.active = 'changer1'
        finish = 0

    if type_screen == 'menu':
        screen.fill((0, 0, 0))
        keys = pg.key.get_pressed()
        for menu in menus:
            menu.update(keys, key0)
            menu.draw(screen)

        for menu in menus:
            if menu.menu_status:
                break
        else:
            for menu in menus:
                if menu.active == 'button_ok':
                    platforms.append(Platform(menu))
                    vorota.append(Vorota(menu.num))
            type_screen = ''
            start = 1

        pg.display.flip()
        clock.tick(60)

        key0 = pg.key.get_pressed()
        continue

    screen.fill((0, 0, 0))
    ball.update(platforms + walls, vorota)
    keys = pg.key.get_pressed()

    for platform in platforms:
        platform.update(keys, key0)

    for vorot in vorota:
        vorot.draw(screen)
        if vorot.score >= 300:
            type_screen = 'menu'
            finish = 1
    for platform in platforms:
        platform.draw(screen)
    ball.draw(screen)
    pg.display.flip()

    key0 = pg.key.get_pressed()

    if start:
        sleep(2)
        start = 0

    clock.tick(60)
