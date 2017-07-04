#!/usr/bin/python3

import pygame, sys, json
from pygame.locals import *

class Snake:
    def __init__(self, tiles = (20, 20), tile_size = 20):
        self.tiles_x = tiles[0]
        self.tiles_y = tiles[1]
        self.tile_size = 20
        self.screen = (self.tiles_x * self.tile_size, self.tiles_y * self.tile_size)

        self.state = {
            "config": {
                "tiles-x": self.tiles_x,
                "tiles-y": self.tiles_y,
                "tile-size": self.tile_size
            },
            "state": {}
        }

    def _save_state(self):
        print(json.dumps(self.state))

    def load(self, text):
        self.state = json.loads(text)

    def _quit(self):
        self._save_state()
        pygame.quit()
        sys.exit()

    def _loop(self):
        for event in self.events:
            pass

    def run(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.screen)
        pygame.display.set_caption("Snake")

        while True:
            self.events = pygame.event.get()

            if QUIT in [e.type for e in self.events]:
                self._quit()

            self._loop()
            pygame.display.update()

if __name__ == "__main__":
    game = Snake((20, 20), 20)
    game.run()
