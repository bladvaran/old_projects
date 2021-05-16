import pygame
from shashki_obj import *
pygame.init()

h = 600
w = 600

key = pygame.key.get_pressed()
pole = Pole()
screen = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

    if (pygame.key.get_pressed()[pygame.K_F12]) and (key[pygame.K_F12] == 0):
        pole.perevorot()
    screen.fill((235, 176, 117))
    pole.update(pygame.key.get_pressed(), key)
    doska_draw(screen, pole)
    pole.shaski_draw(screen)
    pygame.display.update()
    key = pygame.key.get_pressed()
    clock.tick(60)