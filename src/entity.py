from blessed.formatters import FormattingString

class Entity:
    """
    Generic entity object to represent player, enemies, items, etc
    """

    def __init__(self, x: int, y: int, glyph: str, color: FormattingString):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
