#!/usr/bin/python3

import pygame, sys, itertools, time
from pygame.locals import *
from pygame import K_ESCAPE, K_F5
from math import floor
from random import randint

from buttons import ButtonRegistry

tiles_x = tiles_y = 20
background_color = (180, 180, 180)
button_color = (140, 140, 140)
colors = { "text_bomb": (255, 0, 0), "text_btn": (0, 0, 0) }
tile_size = 16
header_size = 40
bomb_count = 20

space_x, space_y = 50, 50
space_btn_x, space_btn_y = 10, 10
btn_size = 50

[RUNNING, WIN, LOSE] = range(3)

def load_sprites(path, xtiles, ytiles, names):
    sprite_img = pygame.image.load(path)
    sprites = {}
    for y, x in itertools.product(range(ytiles), range(xtiles)):
        sp = pygame.Surface((tile_size, tile_size))
        sp.blit(sprite_img, (0, 0), (x*tile_size, y*tile_size, tile_size, tile_size))
        sprites[names[xtiles*y + x]] = sp
        if len(sprites) == len(names): break

    sprites["REDO"] = pygame.transform.scale(sprites["REDO"], (tile_size * 2, tile_size * 2))
    sprites["SETTINGS"] = pygame.transform.scale(sprites["SETTINGS"], (tile_size * 2, tile_size * 2))

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
    global mouse_on, grid, flags, game_state, clicked, start_time, settings_open

    mouse_on = None
    game_state = RUNNING
    flags = []
    grid = [[0 for _ in range(tiles_y)] for _ in range(tiles_x)]
    place_bombs()
    start_time = time.time()
    settings_open = False

    render()

def quit():
    pygame.display.iconify()
    pygame.quit()
    sys.exit()

def get_time():
    diff = time.time() - start_time
    return floor(diff / 60), floor(diff % 60)

def render_header():
    # draw the background
    screen.fill(background_color, Rect(0, 0, screen_size[0], header_size))

    div_text   = digit_font.render("-", 4, colors["text_bomb"])
    bombs_text = digit_font.render("%02d/%02d" % (len(flags), bomb_count), 4, colors["text_bomb"])
    time_text  = digit_font.render("%02d:%02d" % get_time(), 4, colors["text_bomb"])

    center_x, center_y = (screen_size[0] / 2, header_size / 2)

    # draw the text
    screen.blit(div_text, (center_x - div_text.get_width() / 2, center_y - div_text.get_height() / 2))
    screen.blit(bombs_text, (center_x - bombs_text.get_width() - 10, center_y - bombs_text.get_height() / 2))
    screen.blit(time_text, (center_x + 10, center_y - time_text.get_height() / 2))

    # draw the buttons
    screen.blit(sprites["REDO"], (screen_size[0] - 4 - 32, 4))
    screen.blit(sprites["SETTINGS"], (4, 4))

def render_settings():
    screen.fill(background_color, Rect(space_x, space_y, screen_size[0] - space_x*2, screen_size[1] - space_y*2))

    text_txt = ["Accept", "Drop"]
    for i in range(2):
        text = digit_font.render(text_txt[i], 4, colors["text_btn"])

        screen.fill(button_color, Rect(space_x + space_btn_x, space_y + space_btn_y + (btn_size + space_btn_y) * i, screen_size[0] - space_x*2 - space_btn_x*2, btn_size))
        screen.blit(text, (space_x + space_btn_x + (-text.get_width() + screen_size[0] - space_x*2 - space_btn_x*2)/2, space_y + space_btn_y + (btn_size + space_btn_y) * i + (btn_size - text.get_height())/2))

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

    if settings_open: render_settings()

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

def settings_accept():
    global settings_open, bomb_count, tiles_x, tiles_y

    bomb_count = settings_config["bomb_count"]
    tiles_x = settings_config["tiles_x"]
    tiles_y = settings_config["tiles_y"]

    init()
    print("ACCEPT!")

def settings_drop():
    global settings_open
    settings_open = False
    print("DROP!")

def open_settings_menu():
    global settings_open, settings_reg, settings_config
    settings_open = True

    btn_accept = ("accept", settings_accept, space_x + space_btn_x, space_y + space_btn_y,              screen_size[0] - space_x*2 - space_btn_x*2, btn_size)
    btn_drop   = ("drop",   settings_drop,   space_x + space_btn_x, space_y + space_btn_y*2 + btn_size, screen_size[0] - space_x*2 - space_btn_x*2, btn_size)

    settings_reg = ButtonRegistry([btn_accept])
    settings_config = {"bomb_count": bomb_count, "tiles_x": tiles_x, "tiles_y": tiles_y}

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

def check_button_press():
    global settings_open
    x,y = pygame.mouse.get_pos()

    if x > 4 and x < 32 + 4 and y > 4 and y < 32 + 4:
        open_settings_menu()

    x = screen_size[0] - x
    if x > 4 and x < 32 + 4 and y > 4 and y < 32 + 4:
        return True
    return False

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


    for evt in events:
        curr_mouse_pos = get_field(pygame.mouse.get_pos())

        if settings_open and evt.type == MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            settings_reg.check(x, y)
        elif game_state == RUNNING and evt.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
            if evt.type == MOUSEBUTTONDOWN:
                mouse_on = curr_mouse_pos
            elif evt.type == MOUSEBUTTONUP:
                if curr_mouse_pos == mouse_on and evt.button in [1, 3]: click(curr_mouse_pos, evt.button == 1)
                mouse_on = None
                if check_button_press():
                    init()
                    return

pygame.init()
pygame.display.set_caption("Minesweeper")

digit_font = pygame.font.Font("res/digit-font.ttf", 24)

sprites = load_sprites("res/tiles.png", 4, 4, ["N", "F", "B", "C", "1", "2", "3", "4", "5", "6", "7", "8", "BOOM", "X", "REDO", "SETTINGS"])

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
