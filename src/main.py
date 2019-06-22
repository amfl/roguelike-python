from blessed import Terminal
import logging
import os
import datetime

from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all

logger = logging.getLogger()
logname = 'gameplay.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(module)s %(levelno)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def gameloop(t: Terminal, entities):
    # For now, the player is simply the first entity.
    player = entities[0]

    closed = False
    frame_count = 0
    while not closed:
        logger.debug(f'frame: {frame_count}')

        # Clear the whole screen
        print(t.clear())

        render_all(t, entities)

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
    entities = [
            Entity(t.width // 2, t.height // 2, '@', None),
            Entity(t.width // 2 + 5, t.height // 2 - 2, '$', None),
        ]

    # Ready the screen for drawing
    print(t.enter_fullscreen())

    with t.hidden_cursor():
        # Handle input immediately
        with t.cbreak():

            # Enter the main game loop
            gameloop(t, entities)

    print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
