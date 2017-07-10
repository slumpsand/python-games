from buttons import ButtonRegistry

def init():
    global rows, reg, drw, accept_rect, drop_rect, range_surf

    # min, max, current, text
    rows = [
        (settings.bomb_range, bomb_count, "Bombs"),
        (settings.col_range,  tiles_x,    "Columns"),
        (settings.row_range,  tiles_y,    "Rows")
    ]

    # get some memorics for the settings
    (outer_side, outer_up) = spacing.outer
    (inner_sied, _) = spacing.inner
    (bottom, between) = spacing.submit

    # subsurface (drw)
    w = screen.get_width()  - outer_side*2
    h = screen.get_height() - outer_up*2
    drw = screen.subsurface((outer_side, outer_up, w, h))

    # [Accept]
    x = inner_side
    y = h - bottom - sprites.accept.get_height()
    accept_rect = Rect((x, y), sprites.accept.get_size())
    btn_accept = "accept", accept_click, accept_rect)

    # [Drop]
    x += sprites.accept.get_width() + between
    y = h - bottom - sprites.drop.get_height()
    drop_rect = Rect((x, y), sprites.drop.get_size())
    btn_drop = "drop", drop_click, drop_rect)

    # [+] / [-]
    range_surf = []
    range_buttons = []
    for i, row in enumerate(row):
        text = font.menu.render()

    buttons = [btn_accept, btn_drop]
    buttons.extend(range_btns)
    reg = ButtonRegistry(buttons)

def update():
    pass

def accept_click():
    pass

def drop_click():
    pass

def draw():
    drw.fill(colors["menu_back"])

    (inner_side, inner_up) = spacing.inner
    (txt_btn, btn_btn, above) = spacing.row
    (bottom, between, height) = spacing.submit

    for i, row in enumerate(rows):
        # 20 Bombs
        text = font.menu.render("%02d %s" % (row[2], row[3]), 4, colors["text_menu"])
        x = inner_side
        y = inner_up + above * i - text.get_height()/2
        drw.blit(text, (x, y))

        # [+]
        x += text.get_width() txt_btn
        y = inner_up + above * i - sprites.plus.get_height()/2
        drw.blit(sprites.plus, (x, y))

        # [-]
        x += sprites.plus.get_width() + btn_btn
        drw.blit(sprites.minus, (x, y))

    # the buttons
    drw.blit(sprites.accept, accept_rect.size)
    drw.blit(sprites.drop, drop_rect.size)

def activate():
    pass
