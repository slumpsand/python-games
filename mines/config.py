from helper import Colors, Spacing, Settings, get_sprites

tiles_x = tiles_y = 20
tile_size = 16

bomb_count = 20
header_size = 40

colors = Colors (
    background = (180, 180, 180),

    text_bomb  = (255, 0, 0),
    text_menu  = (0, 0, 0)
)

spacing = Spacing (
    outer  = (50, 50),
    inner  = (10, 40),
    rows   = (20, 10, 20),
    submit = (10, 20)
)

settings = Settings (
    bomb_range = (10, 100),
    col_range = (10, 40),
    row_range = (10, 20)
)

sprites = get_sprites("res/tiles.png", 4, 16, ["normal", "flag", "bomb", "clear", "one", "two", "three",
    "four", "five", "six", "seven", "eight", "boom", "wrong", "redo", "settings"], ["redo", "settings"])
