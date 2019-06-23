from blessed import Terminal
from blessed.formatters import FormattingString
import logging
import random

from entity import Entity
from game_map import GameMap

logger = logging.getLogger()

def render_all(t: Terminal, game_map: GameMap, entities):
    """
    Renders everything. The whole lot.
    """

    # Define tile colors here to save on memory
    # Don't need them defined in each tile instance
    colors = {
         'dark_wall': FormattingString(t.cyan_on_blue, t.normal),
         'dark_ground': FormattingString(t.green, t.normal),
    }

    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                # TODO: Optimize. Don't need to move to each tile individually.
                print(colors['dark_wall'](t.move(y, x) + '#'))
            else:
                print(colors['dark_ground'](t.move(y, x) + '.'))

    for ent in entities:
        render_entity(t, ent)

def render_entity(t: Terminal, ent: Entity):
        print(ent.color(t.move(ent.y, ent.x) + ent.glyph))

# def clear_all(t: Terminal, entities):
#     for ent in entities:
#         clear_entity(t, ent)

# def clear_entity(t: Terminal, ent: Entity):
#     # erase the character that represents this object
#     print(t.move(ent.y, ent.x) + ' ')
