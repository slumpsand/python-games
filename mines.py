#!/usr/bin/python3

import pygame, sys, itertools
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor

tiles_x = tiles_y = 20
background_color = (180, 180, 180)
text_color = (255, 255, 255)
tile_size = 16
header_size = 40
bomb_count = 20

def load_sprites(path, xtiles, ytiles, names, count):
    sprite_img = pygame.transform.scale(pygame.image.load(path), (tile_size * xtiles, tile_size * ytiles))
    sprites = {}
    for y, x in itertools.product(range(ytiles), range(xtiles)):
        sp = pygame.Surface((tile_size, tile_size))
        sp.blit(sprite_img, (0, 0), (x*tile_size, y*tile_size, tile_size, tile_size))
        sprites[names[xtiles*y + x]] = sp
        if len(sprites) == count: break
    return sprites

def tile(x, y):
    return Rect(x * tile_size, y * tile_size + header_size, tile_size, tile_size)

def get_field(pos):
    return (floor(pos[0] / tile_size), floor((pos[1] - header_size) / tile_size))

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
    # header
    screen.fill(background_color, Rect(0, 0, screen_size[0], header_size))
    text = bold_font.render("%d / %d" % (len(flags), bomb_count), 4, text_color)
    (text_x, text_y) = text.get_size()
    screen.blit(text, ((screen_size[0] - text_x) / 2, (header_size - text_y) / 2))

    # all flags / normal / number fields
    for x, y in itertools.product(range(tiles_x), range(tiles_y)):
        n = grid[x][y]
        if n == 0: img = "N"
        if n in range(1, 9): img = str(n)
        if n == -1: img = "F"

        screen.blit(sprites[img], (x * tile_size, y * tile_size + header_size))

    # currently clicked field
    if mouse_on != None and grid[mouse_on[0]][mouse_on[1]] == 0:
        screen.fill(background_color, tile(mouse_on[0], mouse_on[1]))

def click(pos, is_left):
    print("%s mouse button at (%d, %d)" % ("left" if is_left else "right", pos[0], pos[1]))

def update():
    global mouse_on

    for key in [e.key for e in events if e.type == KEYDOWN]:
        if key == K_ESCAPE: quit()
        if key == K_F5:
            init()
            return True

    should_render = False

    for evt in events:
        curr_mouse_pos = get_field(pygame.mouse.get_pos())

        if evt.type == MOUSEBUTTONDOWN:
            mouse_on = curr_mouse_pos
            should_render = True
        elif evt.type == MOUSEBUTTONUP:
            if curr_mouse_pos == mouse_on and evt.button in [1, 3]: click(curr_mouse_pos, evt.button == 1)
            mouse_on = None
            should_render = True

    return should_render

pygame.init()
pygame.display.set_caption("Minesweeper")

bold_font = pygame.font.SysFont("Ubuntu", 18, True)

sprite_img = pygame.image.load("img/mines_tiles.jpg")
sprites = load_sprites("img/mines_tiles.jpg", 4, 3, ["N", "F", "B", "C", "1", "2", "3", "4", "5", "6", "7", "8"], 12)

screen_size = (tiles_x * tile_size, tiles_y * tile_size + header_size)
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
