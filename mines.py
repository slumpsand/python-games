#!/usr/bin/python3

import pygame, sys, itertools
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor

tiles_x = tiles_y = 20
background_color = (180, 180, 180)
tile_size = 16

def load_sprites(path, xtiles, ytiles, names):
    sprite_img = pygame.transform.scale(pygame.image.load(path), (tile_size * xtiles, tile_size * ytiles))
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
    grid = [[0 for _ in range(tiles_y)] for _ in range(tiles_x)]

    render()

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

def get_field(x, y):
    return (floor(x / tile_size), floor(y / tile_size))

def click(x, y):
    pass

def update():
    global mouse_on

    for key in [e.key for e in events if e.type == KEYDOWN]:
        if key == K_ESCAPE: quit()
        if key == K_F5:
            init()
            return True

    should_render = False

    for typ in [e.type for e in events]:
        if typ == MOUSEBUTTONDOWN:
            (x, y) = pygame.mouse.get_pos()
            mouse_on = get_field(x, y)
            should_render = True
        elif typ == MOUSEBUTTONUP:
            (x, y) = pygame.mouse.get_pos()
            if get_field(x, y) == mouse_on: click(x, y)
            mouse_on = None
            should_render = True

    return should_render

pygame.init()
pygame.display.set_caption("Minesweeper")

sprite_img = pygame.image.load("img/mines_tiles.jpg")
sprites = load_sprites("img/mines_tiles.jpg", 4, 3, ["N", "F", "B", "C", "1", "2", "3", "4", "5", "6", "7", "8"])

screen_size = (tiles_x * tile_size, tiles_y * tile_size)
screen = pygame.display.set_mode(screen_size)

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
