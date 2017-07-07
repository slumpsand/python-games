#!/usr/bin/python3

import pygame, sys, itertools
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor

tiles_x = tiles_y = 20
background_color = (180, 180, 180)
tile_size = 16

def load_sprites(path, xtiles, ytiles, names):
    sprites = {}
    for y, x in itertools.product(range(ytiles), range(xtiles)):
        sp = pygame.Surface((tile_size, tile_size))
        sp.blit(sprite_img, (0, 0), (x*tile_size, y*tile_size, tile_size, tile_size))
        sprites[names[xtiles*y + x]] = sp
    return sprites

def tile(x, y):
    return Rect(x * tile_size, y * tile_size, tile_size, tile_size)

def init():
    global mouse_on, flags, grid

    mouse_on = None
    flags = []
    grid = [[0] * tiles_y] * tiles_x

def quit():
    pygame.display.iconify()
    pygame.quit()
    sys.exit()

def render():
    # all flags / normal / number fields
    for x, y in itertools.product(range(tiles_x), range(tiles_y)):
        n = grid[x][y]
        if n == 0: img = "N"
        if n in range(1, 9): img = str(n)
        if n == -1: img = "F"

        screen.blit(sprites[img], (x * tile_size, y * tile_size))

    # currently clicked field
    if mouse_on != None and grid[mouse_on[0]][mouse_on[1]] == 0:
        screen.fill(background_color, tile(mouse_on[0], mouse_on[1]))

    # todo: bombs if gameover

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
            mouse_on = None

    return True # return weither the screen must be rerendered

pygame.init()

tile_images = pygame.image.load("img/mines_tiles.jpg")
screen_size = (tiles_x * tile_size, tiles_y * tile_size)

sprite_img = pygame.image.load("img/mines_tiles.jpg")
sprites = load_sprites("img/mines_tiles.jpg", 4, 3, ["N", "F", "B", "C", "1", "2", "3", "4", "5", "6", "7", "8"])

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
