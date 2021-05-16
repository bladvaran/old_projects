import pygame as pg
from pygame.locals import *

D = 180
size = (D, int(D / 12 * 13))
cell_x = size[0] / 12
cell_y = size[1] / 13

Gray = Color(132, 132, 130)


class Menu:
    def __init__(self, xy, w, a, s, d, num):

        self.num = num

        self.surface = pg.Surface((size[0], size[1]))
        self.up_key = w
        self.left_key = a
        self.down_key = s
        self.right_key = d
        self.x = xy[0]
        self.y = xy[1]
        self.menu_status = 1

        self.structure = {
            'color_changer': {self.down_key: 'changer1'},
            'changer1': {self.down_key: 'changer2', self.up_key: 'color_changer'},
            'changer2': {self.down_key: 'changer3', self.up_key: 'changer1'},
            'changer3': {self.down_key: 'button_ok', self.up_key: 'changer2'},
            'button_ok': {self.right_key: 'button_no', self.up_key: 'changer3'},
            'button_no': {self.left_key: 'button_ok', self.up_key: 'changer3'}
        }
        self.active = 'changer1'

        self.changer1 = Changer()
        self.changer2 = Changer()
        self.changer3 = Changer()
        self.button_ok = Button('ok')
        self.button_no = Button('no')

    def draw(self, screen):
        self.surface.fill((160, 160, 160))
        offset = 3
        pg.draw.rect(self.surface, (132, 132, 130), Rect(offset, offset, size[0] - offset, size[1] - offset))
        pg.draw.line(self.surface, (0, 0, 0), (size[0] // 4, 2 * offset), (size[0] // 4, size[1] / 13 * 4 - 4 * offset), 2)
        pg.draw.line(self.surface, (0, 0, 0), (2 * offset, size[1] / 13 * 4 - 2 * offset), (size[0] // 4 - 2 * offset, size[1] / 13 * 4 - 2 * offset), 2)
        pg.draw.line(self.surface, (0, 0, 0), (size[0] // 4 + 2 * offset, size[1] / 13 * 4 - 2 * offset), (size[0] - 2 * offset, size[1] / 13 * 4 - 2 * offset), 2)

        s = self.changer1.get_surface(1 if self.active == 'changer1' else 0)
        self.surface.blit(s, (offset + size[0] / 12, offset + size[1] / 13 * 4))

        s = self.changer2.get_surface(1 if self.active == 'changer2' else 0)
        self.surface.blit(s, (offset + size[0] / 12, offset + size[1] / 13 * 6))

        s = self.changer3.get_surface(1 if self.active == 'changer3' else 0)
        self.surface.blit(s, (offset + size[0] / 12, offset + size[1] / 13 * 8))

        s = self.button_ok.get_surface(1 if self.active == 'button_ok' else 0)
        self.surface.blit(s, (2 * cell_x, 10 * cell_y))

        s = self.button_no.get_surface(1 if self.active == 'button_no' else 0)
        self.surface.blit(s, (8 * cell_x, 10 * cell_y))

        if not self.menu_status:
            self.surface.set_alpha(100)
        else:
            self.surface.set_alpha(255)
        screen.blit(self.surface, (self.x - size[0] // 2, self.y - size[1] // 2))

    def update(self, key, key0):
        if not self.menu_status:
            if self.active == 'button_ok':
                self.button_ok.update(key, key0, self.down_key, self)

            if self.active == 'button_no':
                self.button_ok.update(key, key0, self.down_key, self)
            return

        if self.active == 'changer1':
            self.changer1.update(key, key0, self.left_key, self.right_key)

        if self.active == 'changer2':
            self.changer2.update(key, key0, self.left_key, self.right_key)

        if self.active == 'changer3':
            self.changer3.update(key, key0, self.left_key, self.right_key)

        if self.active == 'button_ok':
            self.button_ok.update(key, key0, self.down_key, self)

        if self.active == 'button_no':
            self.button_ok.update(key, key0, self.down_key, self)

        for key_now in [self.left_key, self.right_key, self.up_key, self.down_key]:
            if key[key_now] and not key0[key_now] and self.structure[self.active].get(key_now):
                self.active = self.structure[self.active][key_now]


class Button:
    def __init__(self, type):
        self.type = type

    def get_surface(self, is_active):
        surface = pg.Surface((2 * cell_x, 2 * cell_x))
        surface.fill((168, 168, 165))
        if is_active:
            pg.draw.rect(surface, (255, 255, 0), Rect(0, 0, 2 * cell_x - 1, 2 * cell_x - 1), 4)
        else:
            pg.draw.rect(surface, (0, 0, 0), Rect(0, 0, 2 * cell_x - 1, 2 * cell_x - 1), 4)

        if self.type == 'ok':
            pg.draw.lines(surface, (2, 186, 8), False, [(cell_x / 2, cell_y), (cell_x, 3 * cell_y / 2), (3 * cell_x / 2, cell_y / 2)], 3)
        else:
            pg.draw.line(surface, (158, 17, 17), (cell_x / 2, cell_y / 2), (3 * cell_x / 2, 3 * cell_y / 2), 3)
            pg.draw.line(surface, (158, 17, 17), (3 * cell_x / 2, cell_y / 2), (cell_x / 2, 3 * cell_y / 2), 3)

        return surface

    def update(self, key, key0, key_down, menu):
        if key[key_down] and not key0[key_down]:
            menu.menu_status = 1 if not menu.menu_status else 0


class ColorChanger:
    def __init__(self):
        pass


class Changer:
    def __init__(self):
        self.size = (size[0] / 12 * 10, size[1] / 13)
        self.level = 1

    def update(self, key, key0, left_key, right_key):
        if key[left_key] and not key0[left_key]:
            self.level = max(self.level - 1, 1)
        if key[right_key] and not key0[right_key]:
            self.level = min(self.level + 1, 5)

    def get_surface(self, is_active):
        surface = pg.Surface(self.size)
        surface.fill(Gray)
        surface.blit(Arrow().get_surface(is_active), (0, 0))
        surface.blit(pg.transform.flip(Arrow().get_surface(is_active), 1, 0), (cell_x * 9 - 10, 0))

        surface.blit(self.get_wall(is_active), (2 * cell_x, 0))
        surface.blit(pg.transform.flip(self.get_wall(is_active), 1, 0), (7 * cell_x, 0))
        surface.blit(self.get_level(), (3 * cell_x, 0))

        return surface

    def get_wall(self, is_active):
        surface = pg.Surface((cell_x / 2, cell_y))
        surface.fill(Gray)

        if is_active:
            color = (255, 255, 0)
        else:
            color = (0, 0, 0)

        pg.draw.rect(surface, color, Rect(0, 0, cell_x / 2, cell_y))
        offset = 2
        pg.draw.rect(surface, (255, 117, 24), Rect(offset, offset, cell_x / 2 - 2 * offset, cell_y - 2 * offset))

        return surface

    def get_level(self):
        surface = pg.Surface((4 * cell_x, cell_y))
        surface.fill(Gray)

        one_rect_size = cell_x / 2
        otstup = one_rect_size / 2

        now_x = 0
        offset = 4
        for i in range(5):
            if i < self.level:
                pg.draw.rect(surface, (71, 199, 60), Rect(now_x, 0, one_rect_size, cell_y))
                pg.draw.rect(surface, (139, 229, 131), Rect(now_x + one_rect_size / 2, 2, one_rect_size / 2, cell_y - 2 * offset))
            else:
                pg.draw.rect(surface, (75, 89, 74), Rect(now_x, 0, one_rect_size, cell_y))
                pg.draw.rect(surface, (143, 161, 141), Rect(now_x + one_rect_size / 2, 2, one_rect_size / 2, cell_y - 2 * offset))
            now_x += one_rect_size + otstup
        return surface


class Arrow:
    def __init__(self):
        self.size = size[1] / 13  # размер основания треугольника
        self.H = 20  # высота до основания треугольника
        self.surface = pg.Surface((self.H, self.size))

    # стрелка влево
    def get_surface(self, is_active):
        if is_active:
            color = (255, 255, 0)
        else:
            color = (0, 0, 0)

        self.surface.fill(Gray)
        offset = 4
        pg.draw.polygon(self.surface, color, [(0, self.size / 2), (self.H, 0), (self.H, self.size)])
        pg.draw.polygon(self.surface, (255, 153, 0), [(offset + 2, self.size / 2), (self.H - offset + 1, offset), (self.H - offset + 1, self.size - offset)])
        return self.surface
