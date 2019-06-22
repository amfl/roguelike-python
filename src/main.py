from blessed import Terminal
import logging
import os
import datetime

from input_handlers import handle_keys

logger = logging.getLogger()
logname = 'gameplay.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(module)s %(levelno)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def gameloop(t: Terminal):
    closed = False
    playerpos = (t.width // 2, t.height // 2)
    frame_count = 0
    while not closed:
        logger.debug(f'frame: {frame_count}')

        # Clear the whole screen
        print(t.clear())

        # Print the player
        print(t.move(playerpos[1], playerpos[0]) + '@')

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
            playerpos = (
                    playerpos[0] + move[0],
                    playerpos[1] + move[1]
                )

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

    print(t.enter_fullscreen())

    with t.hidden_cursor():
        # Handle input immediately
        with t.cbreak():
            gameloop(t)

    print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
