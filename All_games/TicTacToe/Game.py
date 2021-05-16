import pygame
import random
from Tic_Tac_Toe_OBJ import *
pygame.init()

pred = 'P1'
w = 500
h = 500
while 1:

    pole = Pole()
    pole.hod = pred
    pred = men(pred)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((w, h))
    key1 = pygame.key.get_pressed()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        key = pygame.key.get_pressed()
        screen.fill((255, 232, 158))

        pole.draw(screen)
        pole.update(key, key1, screen)

        pygame.display.update()
        key1 = pygame.key.get_pressed()
        clock.tick(60)
        if pole.k > 400:
            pygame.time.wait(500)
            break
