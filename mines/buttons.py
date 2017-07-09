from pygame import Rect

class Button:
    def __init__(self, name, x, y, width, height, callback=None):
        self.name = name
        self.callback = callback
        self.x = x
        self.y = y
        self.x2 = x+width
        self.y2 = y+height

class ButtonRegistry:
    def __init__(self, btns=[]):
        self.btns = []
        self.state = {}
        for b in btns: self.add(b)

    def add(self, b):
        self.state[b[0]] = False

        if b is Button:
            self.btns.append(b)
        elif b[0] is Rect:
            self.btns.append(Button(b[0], b[2].left, b[2].top, b[2].width, b[2].height, b[1]))
        else:
            self.btns.append(Button(b[0], b[2], b[3], b[4], b[5], b[1]))

    def check(self, x, y):
        self.state = {b.name: False for b in self.btns}

        for b in self.btns:
            if x > b.x and x < b.x2 and y > b.y and y < b.y2:
                self.state[b.name] = True
                b.callback()
