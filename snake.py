#!/usr/bin/python3

import pygame, sys
from pygame.locals import *
from pygame import K_LEFT, K_RIGHT, K_DOWN, K_UP, K_ESCAPE, K_F5
from random import randint
from time import sleep

[UP, RIGHT, DOWN, LEFT] = range(4)

# settings
tiles_x = tiles_y = 21
tile_size = 20
start_tiles = 6
background_color = (0, 0, 0)
apple_color = (255, 0, 0)
snake_color = (0, 255, 0)
head_color = (0, 150, 0)
gameover_color = (255, 0, 0)
score_color = (255, 255, 255)
fps = 8
# end settings

screen_size = (tile_size * tiles_x, tile_size * tiles_y)

def init():
    global apples, snake, is_alive, score, facing

    apples = []
    facing = UP
    is_alive = True
    score = 0

    mid = (round(tiles_x / 2), round(tiles_y / 2))
    snake = [(mid[0], mid[1] + x) for x in range(start_tiles)]

    spawn_apple()

def quit():
    pygame.display.iconify()
    pygame.quit()
    sys.exit()

def render():
    screen.fill(background_color)

    for (x, y) in apples: screen.fill(apple_color, Rect(x * tile_size, y * tile_size, tile_size, tile_size))
    for (x, y) in snake[1:]: screen.fill(snake_color, Rect(x * tile_size, y * tile_size, tile_size, tile_size))
    screen.fill(head_color, Rect(snake[0][0] * tile_size, snake[0][1] * tile_size, tile_size, tile_size))

    if not is_alive:
        text = gameover_font.render("Game Over!", 1, gameover_color)
        (_, _, x, y) = text.get_rect()
        screen.blit(text, ((screen_size[0] - x) / 2, (screen_size[1] - y) / 2))

    screen.blit(basic_font.render("Score: %d" % score, 1, score_color), (10, 10))

def update():
    global apples, snake, is_alive, score, facing

    for key in [e.key for e in events if e.type == KEYDOWN]:
        if key == K_LEFT and facing != RIGHT: facing = LEFT
        if key == K_RIGHT and facing != LEFT: facing = RIGHT
        if key == K_DOWN and facing != UP: facing = DOWN
        if key == K_UP and facing != DOWN: facing = UP

        if key == K_ESCAPE: quit()
        if key == K_F5:
            init()
            return

    if not is_alive: return

    (x, y) = snake[0]

    if facing == LEFT: pos = (x-1, y)
    if facing == RIGHT: pos = (x+1, y)
    if facing == UP: pos = (x, y-1)
    if facing == DOWN: pos = (x, y+1)

    if pos[0] < 0 or pos[0] >= tiles_x or pos[1] < 0 or pos[1] >= tiles_y or pos in snake:
        is_alive = False
        return

    snake.insert(0, pos)

    has_apple = False
    for i in range(len(apples)):
        if apples[i] in snake:
            has_apple = True
            del apples[i]
            spawn_apple()
            score += 1

    if not has_apple:
        snake.pop()

def spawn_apple():
    global apples

    pos = (randint(0, tiles_x - 1), randint(0, tiles_y - 1))
    if pos in snake or pos in apples: spawn_apple()
    else: apples.append(pos)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Snake")

    basic_font = pygame.font.SysFont("Monospace", 20)
    gameover_font = pygame.font.SysFont("Monospace", 60)

    init()

    should_stop = False
    while not should_stop:
        global events
        events = pygame.event.get()

        if QUIT in [e.type for e in events]:
            quit()

        # swap these two?
        update()
        render()

        pygame.display.update()
        sleep(1 / fps)
