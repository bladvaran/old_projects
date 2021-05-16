import pygame
from o2048 import *
pygame.init()

h = 600
w = 600

pole = Pole()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((w, h))
key2 = pygame.key.get_pressed()
pole.pole[3][3].pusto = 0
pole.pole[3][0].pusto = 0
pole.pole[3][0].chislo = 4

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    key1 = pygame.key.get_pressed()

    pole.update(key1, key2)

    screen.fill((255, 255, 255))
    pole.draw_p(screen)
    pygame.display.update()

    key2 = pygame.key.get_pressed()
    clock.tick(60)

