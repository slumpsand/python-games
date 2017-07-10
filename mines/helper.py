from collections import namedtuple
import pygame

# outer:  (hori, vert)
# inner:  (hori, vert)
# rows:   (text_btn, btn_btn, above)
# submit: (bottom, between)
Spacing = namedtuple("Spacing", "outer inner rows submit")

Colors = namedtuple("Colors", "background text_bomb text_menu menu_back")

# bomb_range: (min_bomb, max_bomb)
# col_range:  (min_col, max_col)
# row_range:  (min_row, max_row)
Settings = namedtuple("Settings", "bomb_range col_range row_range")

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

    # redo, settings

    # plus, minus

    return sprites
