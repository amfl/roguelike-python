from blessed import Terminal
from blessed.formatters import FormattingString
import logging
import os
import datetime
import sys

from components.ai import BasicMonster
from components.fighter import Fighter
from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from game_map import GameMap
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import render_all, clear_all

logger = logging.getLogger()
logname = 'gameplay.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(module)s %(levelno)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def game_loop(
        t: Terminal,
        game_map: GameMap,
        entities,
        fov_map
):
    # For now, the player is simply the first entity.
    player = entities[0]

    closed = False
    frame_count = 0
    fov_recompute = True

    game_state = GameStates.PLAYERS_TURN

    while not closed:
        logger.debug(f'frame: {frame_count}')

        clear_all(t, entities)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, 3)

        # Enemies move before the screen renders
        if game_state == GameStates.ENEMY_TURN:
            for e in entities:
                if e.ai:
                    e.ai.take_turn()
            game_state = GameStates.PLAYERS_TURN

        render_all(t, game_map, entities, fov_map, fov_recompute)

        sys.stdout.flush()

        # Read in input for a new turn.
        fov_recompute = False
        inp = t.inkey()
        logger.debug('Key Input: ' + repr(inp))
        action = handle_keys(inp)
        logger.debug('Action: ' + repr(action))

        exit = action.get('exit')
        move = action.get('move')

        # Escape key doesn't work and I don't know why.
        if exit:
            logger.info('Quitting cleanly...')
            closed = True
            return True

        if move and game_state == GameStates.PLAYERS_TURN:
            destination = (
                player.x + move[0],
                player.y + move[1],
            )
            if not game_map.is_blocked(destination[0], destination[1]):
                # Try to push anything that is there
                [e.push(game_map, move[0], move[1]) for e in entities if e.x == destination[0] and e.y == destination[1]]

                blocking_ent = Entity.get_blocking_entity_at_location(entities, destination[0], destination[1])
                if blocking_ent:
                    logger.debug("Bonked into a blocking entity: %s", blocking_ent.name)
                else:
                    # Update player position
                    player.move(move[0], move[1])
                    fov_recompute = True
            game_state = GameStates.ENEMY_TURN

        frame_count += 1

def main():
    t = Terminal()

    # Prelude
    logger.info("----------------------------------")
    logger.info("Starting new run.")
    logger.info("Datetime: %s", datetime.datetime.now().isoformat())
    logger.info("Revision: %s", os.getenv('REVISION'))
    logger.info("Terminal colors: %d", t.number_of_colors)
    logger.info("Terminal size: %dx%d", t.width, t.height)
    logger.info("----------------------------------")
    #

    # Create the world
    map_dimensions = (20, 12)

    if t.width < map_dimensions[0] or t.height < map_dimensions[1]:
        logger.fatal("Terminal too small: Must be at least %dx%d in size.",
               map_dimensions[0], map_dimensions[1])
        sys.exit(1)

    game_map = GameMap(map_dimensions[0], map_dimensions[1])
    game_map.make_map()

    fov_map = initialize_fov(game_map)

    entities = [
            Entity(
                4, 4, '@', 'Player',
                FormattingString(t.red, t.normal),
                fighter=Fighter(
                    hp=30,
                    defense=2,
                    power=5
                )),
            Entity(
                map_dimensions[0] // 2 + 5,
                map_dimensions[1] // 2 - 2,
                '$', 'Mysterious Object',
                FormattingString(t.yellow, t.normal)),
            Entity(
                3, 3, '%', 'Crate',
                FormattingString(t.blue, t.normal),
                pushable=True),
            Entity(
                10, 5, 'o', 'Goblin',
                FormattingString(t.green, t.normal),
                fighter=Fighter(
                    hp=16,
                    defense=1,
                    power=3
                ),
                ai=BasicMonster())
        ]

    # Ready the screen for drawing
    print(t.enter_fullscreen())

    with t.hidden_cursor():
        # Handle input immediately
        with t.cbreak():

            # Enter the main game loop
            game_loop(t, game_map, entities, fov_map)

    print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
