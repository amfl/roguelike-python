from blessed.formatters import FormattingString
from game_map import GameMap
from components.fighter import Fighter
from components.ai import BasicMonster

import logging
import math

logger = logging.getLogger()

class Entity:
    """
    Generic entity object to represent player, enemies, items, etc
    """

    def __init__(
            self,
            x: int, y: int,
            glyph: str,
            name: str,
            color: FormattingString,
            pushable: bool = False,
            blocking: bool = True,
            fighter: Fighter = None,
            ai: BasicMonster = None
    ):
        self.x = x
        self.y = y
        self.glyph = glyph
        self.color = color
        self.name = name
        self.pushable = pushable
        self.blocking = blocking
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def push(self, game_map: GameMap, x_delta: int, y_delta: int):
        """
        Attempts to push this in a direction.
        Returns true if push was successful.
        """
        if self.pushable:
            x_new = self.x + x_delta
            y_new = self.y + y_delta
            if not game_map.is_blocked(x_new, y_new):
                self.move(x_delta, y_delta)
                return True
        return False

    def get_blocking_entity_at_location(entities, x_dest, y_dest):
        for e in entities:
            if e.blocking:
                if e.x == x_dest and e.y == y_dest:
                    return e
        return None

    def move_towards(self, game_map: GameMap, entities, x_target: int, y_target: int):
        dx = x_target - self.x
        dy = y_target - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    Entity.get_blocking_entity_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
