#!/usr/bin/python3

import pygame, sys, json, time
from pygame.locals import *
from math import ceil
from random import randint

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

class Snake:
    def __init__(self):
        # initialize all constant variables
        self.tiles_x = 20
        self.tiles_y = 20
        self.tile_size = 20
        self.start_tiles = 6
        self.background_color = Color(0, 0, 0, 255)
        self.apple_color = Color(255, 0, 0, 255)
        self.snake_color = Color(0, 255, 0, 255)
        self.fps = 8

    def set_tiles(self, x, y):
        self.tiles_x = x
        self.tiles_y = y
        return self

    def set_tile_size(self, tile_size):
        self.tile_size = tile_size
        return self

    def set_start_tiles(self, start_tiles):
        self.start_tiles = start_tiles
        return self

    def set_colors(self, back, snake, apple):
        self.background_color = back
        self.snake_color = snake
        self.apple_color = apple
        return self

    def set_fps(self, fps):
        self.fps = fps
        return self

    def _init(self):
        # initialize variables
        self.screen = (self.tiles_x * self.tile_size, self.tiles_y * self.tile_size)
        self.snake = []
        self.apples = []
        self.dir = UP
        self.is_alive = True
        self.score = 0

        # create the snake
        mid = (ceil(self.tiles_x / 2), ceil(self.tiles_y / 2))
        self.snake.extend((mid[0], mid[1] + i) for i in range(self.start_tiles))

        # spawn the first apple
        self._spawn_apple()

        # initialize pygame
        pygame.init()
        self.surface = pygame.display.set_mode(self.screen)
        pygame.display.set_caption("Snake")

        self.font = pygame.font.SysFont("monospace", 20)
        self.gameover = pygame.font.SysFont("monospace", 60)

    def _spawn_apple(self):
        pos = (randint(0, self.tiles_x-1), randint(0, self.tiles_y-1))
        if pos in self.snake: self._spawn_apple()
        else: self.apples.append(pos)

    def _render(self):
        for event in self.events:
            pass

        self.surface.fill(self.background_color)
        for (x, y) in self.apples: self.surface.fill(self.apple_color, Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
        for (x, y) in self.snake:  self.surface.fill(self.snake_color, Rect(x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))

        if not self.is_alive:
            self.surface.blit(self.gameover.render("GAME OVER!", 1, (255, 0, 0)), (self.screen[0] / 2 - 175, self.screen[1] / 2 - 30))

        self.surface.blit(self.font.render("Score: %d" % self.score, 1, (255, 255, 255)), (10, 10))

    def _quit(self):
        pygame.display.iconify()
        pygame.quit()
        sys.exit()

    def _update(self):
        for evt in self.events:
            if evt.type == KEYDOWN:
                if evt.key == pygame.K_LEFT and self.dir != RIGHT:
                    self.dir = LEFT

                if evt.key == pygame.K_RIGHT and self.dir != LEFT:
                    self.dir = RIGHT

                if evt.key == pygame.K_UP and self.dir != DOWN:
                    self.dir = UP

                if evt.key == pygame.K_DOWN and self.dir != UP:
                    self.dir = DOWN

                if evt.key == pygame.K_F5:
                    self._init()
                    return

                if evt.key == pygame.K_ESCAPE:
                    self._quit()

        if not self.is_alive:
            return

        front = self.snake[0]

        if self.dir == LEFT:
            pos = (front[0]-1, front[1])
            if pos[0] < 0: self.is_alive = False
        if self.dir == RIGHT:
            pos = (front[0]+1, front[1])
            if pos[0] >= self.tiles_x: self.is_alive = False
        if self.dir == UP:
            pos = (front[0], front[1]-1)
            if pos[1] < 0: self.is_alive = False
        if self.dir == DOWN:
            pos = (front[0], front[1]+1)
            if pos[1] >= self.tiles_y: self.is_alive = False

        has_apple = False
        for i in range(len(self.apples)):
            if self.apples[i] in self.snake:
                has_apple = True
                del self.apples[i]
                self._spawn_apple()
                self.score += 1

        if self.is_alive:
            self.snake.insert(0, pos)
            if not has_apple:
                self.snake.pop()

    def run(self):
        self._init()

        while True:
            self.events = pygame.event.get()

            if QUIT in [e.type for e in self.events]:
                self._quit()

            self._update()
            self._render()
            pygame.display.update()
            time.sleep(1 / self.fps)

if __name__ == "__main__":
    Snake().run()
