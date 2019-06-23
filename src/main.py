from blessed import Terminal
from blessed.formatters import FormattingString
import logging
import os
import datetime
import sys

from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all
from game_map import GameMap

logger = logging.getLogger()
logname = 'gameplay.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(module)s %(levelno)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def game_loop(t: Terminal, game_map: GameMap, entities):
    # For now, the player is simply the first entity.
    player = entities[0]

    closed = False
    frame_count = 0
    while not closed:
        logger.debug(f'frame: {frame_count}')

        # Clear the whole screen
        print(t.clear())

        render_all(t, game_map, entities)

        sys.stdout.flush()

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

        if move:
            destination = (
                player.x + move[0],
                player.y + move[1],
            )
            if not game_map.is_blocked(destination[0], destination[1]):
                # Update player position
                player.move(move[0], move[1])

        frame_count += 1

def main():
    t = Terminal()

    # Prelude
    logger.info("----------------------------------")
    logger.info("Starting new run.")
    logger.info("Datetime: %s", datetime.datetime.now().isoformat())
    logger.info("Revision: %s", os.getenv('REVISION'))
    logger.info("Terminal colors: %d", t.number_of_colors)
    logger.info("----------------------------------")
    #

    # Create the world
    map_dimensions = (12, 12)

    game_map = GameMap(map_dimensions[0], map_dimensions[1])

    entities = [
            Entity(
                map_dimensions[0] // 2,
                map_dimensions[1] // 2,
                '@',
                FormattingString(t.red, t.normal)),
            Entity(
                map_dimensions[0] // 2 + 5,
                map_dimensions[1] // 2 - 2,
                '$',
                FormattingString(t.yellow, t.normal)),
        ]

    # Ready the screen for drawing
    print(t.enter_fullscreen())

    with t.hidden_cursor():
        # Handle input immediately
        with t.cbreak():

            # Enter the main game loop
            game_loop(t, game_map, entities)

    print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
