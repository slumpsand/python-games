from helper import Colors, Menu, get_sprites

tiles_x = tiles_y = 20
tile_size = 16

bomb_count = 20
header_size = 40

colors = Colors(
    background = (180, 180, 180),
    button = (140, 140, 140), # remove!

    text_bomb = (255, 0, 0),
    text_btn = (0, 0, 0)
)

menu = Menu(
    menu_spacing = (50, 50),
    btn_spacing = (10, 10),
    btn_height = 50
)

sprites = get_sprites("res/tiles.png", 4, 16, ["normal", "flag", "bomb", "clear", "one", "two", "three",
    "four", "five", "six", "seven", "eight", "boom", "wrong", "redo", "settings"], ["redo", "settings"])
