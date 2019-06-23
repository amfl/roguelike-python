from game_objects import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # Start off with an empty floor everywhere
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        # Randomly draw some junk.
        # TODO: This will crash with small maps.
        for y in range(3):
            tiles[y+4][10].blocked = True
            tiles[y+4][10].block_sight = True

        return tiles
