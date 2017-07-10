from collections import namedtuple
import pygame

Colors = namedtuple("Colors", "background button text_bomb text_btn")
Menu = namedtuple("Menu", "menu_spacing btn_spacing btn_height")
class Sprites: pass

def get_sprites(path, width, size, names, doubles):
    sprite_img = pygame.image.load(path)
    sprites = Sprites()
    for (i, name) in enumerate(names):
        x, y = i % width, int(i / width)
        sp = pygame.Surface((size, size))
        sp.blit(sprite_img, (0, 0), (x*size, y*size, size, size))
        if name in doubles: sp = pygame.transform.scale(sp, (size*2, size*2))
        setattr(sprites, name, sp)

    return sprites
