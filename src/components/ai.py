from game_map import GameMap

import logging
import tcod

logger = logging.getLogger()

class BasicMonster:
    # Can't specify that `target` is an entity because cyclic dependencies...
    def take_turn(self, target, fov_map, game_map: GameMap, entities):
        # Owner is set by entity constructor... Don't know if I like that
        # Can't dynamically add components without bookkeeping :(
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_towards(game_map, entities, target.x, target.y)
            elif target.fighter.hp > 0:
                logger.info("The %s is close enough to attack you!", monster.name)
