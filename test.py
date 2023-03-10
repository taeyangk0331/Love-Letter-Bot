class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rect(Position):
    width : int
    height : int

    def __init__(self, x, y, width, height):
        super().__init__(x, y)
        self.width = width
        self.height = height

position = Position(0, 0)
rect = Rect(0, 0, 100, 50)
print(rect.x, rect.y, rect.width, rect.height)