#!/usr/bin/python3

import pygame, sys
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor

tiles_x = tiles_y = 20
background_color = (100, 100, 100)
tile_color = (150, 150, 150)

pygame.init()

tile_image = pygame.image.load("img/mines_tile.png")
tile_size = tile_image.get_size()[0]

screen_size = (tiles_x * tile_size, tiles_y * tile_size)

def init():
    global mouse_on

    mouse_on = (None, None)

def quit():
    pygame.display.iconify()
    pygame.quit()
    sys.exit()

def render():
    screen.fill(background_color)
    for x in range(tiles_x):
        for y in range(tiles_y):
            screen.blit(tile_image, (x * tile_size, y * tile_size))

def get_field(x, y):
    return (floor(x / tile_size), floor(y / tile_size))

def update():
    global mouse_on

    for key in [e.key for e in events if e.type == KEYDOWN]:
        if key == K_ESCAPE: quit()
        if key == K_F5:
            init()
            return True

    for typ in [e.type for e in events]:
        if typ == MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            mouse_on = get_field(x, y)
        elif typ == MOUSEBUTTONUP:
            (x, y) = pygame.mouse.get_pos()
            if get_field(x, y) == mouse_on:
                print("user clicked field %s" % str(mouse_on))

    return True # return weither the screen must be rerendered

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Minesweeper")

init()

try:
    while True:
        global events
        events = pygame.event.get()

        if QUIT in [e.type for e in events]:
            quit()

        if update(): render()
        pygame.display.update()
except KeyboardInterrupt:
    quit()
