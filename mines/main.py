#!/usr/bin/python3

import pygame, sys, itertools, time
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor
from random import randint

tiles_x = tiles_y = 20
background_color = (180, 180, 180)
colors = { "text_bomb": (255, 0, 0) }
tile_size = 16
header_size = 40
bomb_count = 20

[RUNNING, WIN, LOSE] = range(3)

def load_sprites(path, xtiles, ytiles, names):
    sprite_img = pygame.transform.scale(pygame.image.load(path), (tile_size * xtiles, tile_size * ytiles))
    sprites = {}
    for y, x in itertools.product(range(ytiles), range(xtiles)):
        sp = pygame.Surface((tile_size, tile_size))
        sp.blit(sprite_img, (0, 0), (x*tile_size, y*tile_size, tile_size, tile_size))
        sprites[names[xtiles*y + x]] = sp
        if len(sprites) == len(names): break
    return sprites

def tile(x, y):
    return Rect(x * tile_size, y * tile_size + header_size, tile_size, tile_size)

def get_field(pos):
    x, y = floor(pos[0] / tile_size), floor((pos[1] - header_size) / tile_size)
    if x < 0 or y < 0 or x >= tiles_x or y >= tiles_y:
        return None
    return x, y

def place_bombs():
    global bombs
    bombs = []

    while len(bombs) < bomb_count:
        b = randint(0, tiles_x-1), randint(0, tiles_y-1)
        if not b in bombs: bombs.append(b)

def init():
    global mouse_on, grid, flags, game_state, clicked, start_time

    mouse_on = None
    game_state = RUNNING
    flags = []
    grid = [[0 for _ in range(tiles_y)] for _ in range(tiles_x)]
    place_bombs()
    start_time = time.time()

    render()

def quit():
    pygame.display.iconify()
    pygame.quit()
    sys.exit()

def get_time():
    diff = time.time() - start_time
    return floor(diff / 60), floor(diff % 60)

def render_header():
    screen.fill(background_color, Rect(0, 0, screen_size[0], header_size))

    div_text   = digit_font.render("-", 4, colors["text_bomb"])
    bombs_text = digit_font.render("%02d/%02d" % (len(flags), bomb_count), 4, colors["text_bomb"])
    time_text  = digit_font.render("%02d:%02d" % get_time(), 4, colors["text_bomb"])

    center_x, center_y = (screen_size[0] / 2, header_size / 2)

    screen.blit(div_text, (center_x - div_text.get_width() / 2, center_y - div_text.get_height() / 2))
    screen.blit(bombs_text, (center_x - bombs_text.get_width() - 10, center_y - bombs_text.get_height() / 2))
    screen.blit(time_text, (center_x + 10, center_y - time_text.get_height() / 2))

def render():
    # header
    if game_state == RUNNING: render_header()

    # all flags / normal / number fields
    for x, y in itertools.product(range(tiles_x), range(tiles_y)):
        n = grid[x][y]

        if n in range(1, 9): img = str(n)
        if n == 0: img = "N"
        if n == -1: img = "F"
        if n == -2: img = "B"
        if n == -3: img = "C"
        if n == -4: img = "BOOM"
        if n == -5: img = "X"

        screen.blit(sprites[img], (x * tile_size, y * tile_size + header_size))

    # currently clicked field
    if mouse_on != None and grid[mouse_on[0]][mouse_on[1]] == 0:
        screen.fill(background_color, tile(mouse_on[0], mouse_on[1]))

def solve_all():
    for x,y in itertools.product(range(tiles_x), range(tiles_y)):
        if (x, y) in bombs:
            grid[x][y] = -2
            continue

        count = 0
        for b in [(a,b) for (a,b) in itertools.product(range(x-1, x+2), range(y-1, y+2)) if (a != x or b != y) and a >= 0 and b >= 0 and a < tiles_x and b < tiles_y]:
            if b in bombs: count += 1

        grid[x][y] = -3 if count == 0 else count

def show_bombs():
    for x,y in itertools.product(range(tiles_x), range(tiles_y)):
        if (x, y) in bombs:
            grid[x][y] = -2

    for (x,y) in flags:
        if not (x,y) in bombs:
            grid[x][y] = -5

def unwrap(x, y):
    if (x, y) in bombs: return
    in_range = [(a,b) for (a,b) in itertools.product(range(x-1, x+2), range(y-1, y+2)) if (a != x or b != y) and a >= 0 and b >= 0 and a < tiles_x and b < tiles_y]

    # count the bombs in range
    count = 0
    for bx,by in in_range:
        if (bx,by) in bombs: count += 1

    if count == 0:
        grid[x][y] = -3

        for (px,py) in in_range:
            if grid[px][py] == 0: unwrap(px, py)
    else:
        grid[x][y] = count

def click(pos, is_left):
    global game_state

    if pos == None:
        return

    if is_left:
        if pos in bombs:
            game_state = LOSE
            show_bombs()
            grid[pos[0]][pos[1]] = -4
        else:
            unwrap(pos[0], pos[1])
    else:
        if grid[pos[0]][pos[1]] in [0, -1]:
            if grid[pos[0]][pos[1]] == -1:
                flags.remove(pos)
                grid[pos[0]][pos[1]] = 0
            else:
                flags.append(pos)
                grid[pos[0]][pos[1]] = -1

def update():
    global mouse_on, game_state

    if sorted(bombs) == sorted(flags) and game_state == RUNNING:
        solve_all()
        game_state = WIN

    for key in [e.key for e in events if e.type == KEYDOWN]:
        if key == K_ESCAPE: quit()
        if key == K_F5:
            init()
            return

    if game_state != RUNNING:
        return

    for evt in events:
        curr_mouse_pos = get_field(pygame.mouse.get_pos())

        if evt.type == MOUSEBUTTONDOWN:
            mouse_on = curr_mouse_pos
        elif evt.type == MOUSEBUTTONUP:
            if curr_mouse_pos == mouse_on and evt.button in [1, 3]: click(curr_mouse_pos, evt.button == 1)
            mouse_on = None

pygame.init()
pygame.display.set_caption("Minesweeper")

digit_font = pygame.font.Font("res/digit-font.ttf", 24)

sprites = load_sprites("res/tiles.jpg", 4, 4, ["N", "F", "B", "C", "1", "2", "3", "4", "5", "6", "7", "8", "BOOM", "X"])

text_sizes = {"bombs": digit_font.render("00/00", 4, (0, 0, 0)).get_size(), "time": digit_font.render("00:00", 4, (0, 0, 0)).get_size() }


screen_size = (tiles_x * tile_size, tiles_y * tile_size + header_size)
screen = pygame.display.set_mode(screen_size)

init()

try:
    while True:
        global events
        events = pygame.event.get()

        if QUIT in [e.type for e in events]:
            quit()

        update()
        render()

        pygame.display.update()
except KeyboardInterrupt:
    quit()
