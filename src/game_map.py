from game_objects import Tile
from map_objects import Rect

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        # Start off with an empty floor everywhere
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        # Randomly draw some junk.
        # TODO: This will crash with small maps.
        for x in range(3):
            tiles[x+4][10].blocked = True
            tiles[x+4][10].block_sight = True

        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def make_map(self):
        # Create two rooms for demonstration purposes
        room1 = Rect(2, 2, 4, 4)
        room2 = Rect(8, 2, 4, 4)

        self.create_room(room1)
        self.create_room(room2)

        # Join the two rooms with a tunnel
        self.create_h_tunnel(3, 8, 3)

    def create_room(self, room: Rect):
        # Make all tiles in the rectangle passable
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
