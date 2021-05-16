import pygame
from saper_obj import *
pygame.init()

h = 500
w = 500
while 1:
    f = 0
    pole = Pole()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 500))

    key1 = pygame.key.get_pressed()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        mouse = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()
        screen.fill((200, 200, 200))
        f = pole.update(mouse, key, key1)
        pole.draw(screen)

        key1 = pygame.key.get_pressed()
        pygame.display.update()
        if f == 1:
            break
        clock.tick(60)
