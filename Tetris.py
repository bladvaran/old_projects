import pygame
import random
from obekti import *
pygame.init()

n = 60
h = 640
w = 480
a = []
a.append(add())
figure = a[0]
pole = Pole()
i = 1
clock = pygame.time.Clock()
screen = pygame.display.set_mode((480, 640))
VNIZ = pygame.USEREVENT + 1

pygame.time.set_timer(VNIZ, 500)
key = pygame.key.get_pressed()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == VNIZ:
            if n == 60:
                figure.rect[0]['y'] += 20

    if (key[pygame.K_DOWN]):
        n = 61
        figure.rect[0]['y'] += 20
    else:
        n = 60


    figure.update(key, figure)
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (100, 100, 100), (-5, 590, w + 5, h - 580))  # D
    pygame.draw.rect(screen, (120, 120, 120), (-5, -5, 55, h + 5))  # L
    pygame.draw.rect(screen, (120, 120, 120), (w - 50, -5, 60, h + 5))  # R

    for j in range(4):
        pygame.draw.rect(screen, (255, 255, 255), (figure.rect[j]['x'] - 10, figure.rect[j]['y'] - 10, 21, 21), 3)
        pygame.draw.rect(screen, (255, 255, 255), (figure.rect[j]['x'] - 5, figure.rect[j]['y'] - 5, 10, 10))


    key = pygame.key.get_pressed()

    if (figure.rect[0]['y'] >= 580) or (pole.update(figure)):
        pole.kvadratiki.append(figure.rect[0])
        pole.kvadratiki.append(figure.rect[1])
        pole.kvadratiki.append(figure.rect[2])
        pole.kvadratiki.append(figure.rect[3])
        a.append(add())
        figure = a[i]
        i += 1

    pole.printer(screen)
    pygame.display.update()
    pole.prov(screen)
    clock.tick(n)