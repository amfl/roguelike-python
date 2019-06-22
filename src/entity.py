class Entity:
    """
    Generic entity object to represent player, enemies, items, etc
    """

    def __init__(self, x, y, glyph, color):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color

    def move(self, x, y):
        self.x += x
        self.y += y
