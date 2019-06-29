import tcod
import logging

logger = logging.getLogger()

def initialize_fov(game_map):
    """
    Called whenever the map changes shape.
    """

    fov_map = tcod.map_new(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight,
                                    not game_map.tiles[x][y].blocked)

    return fov_map

def recompute_fov(fov_map, x, y, radius, light_walls=True, algorithm=0):
    logger.debug("Recomputing FOV...")

    tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
