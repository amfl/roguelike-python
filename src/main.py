from blessed import Terminal
import logging
import os
import datetime

logger = logging.getLogger()
logname = 'gameplay.log'
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(module)s %(levelno)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

def main():
    t = Terminal()
    print(t.enter_fullscreen())

    # Prelude
    logger.info("----------------------------------")
    logger.info("Starting new run.")
    logger.info("Datetime: %s", datetime.datetime.now().isoformat())
    logger.info("Revision: %s", os.getenv('REVISION'))
    logger.info("Terminal colors: %d", t.number_of_colors)
    logger.info("----------------------------------")
    #

    closed = False
    playerpos = (0,0)
    frame_count = 0
    while not closed:
        logger.debug(f'frame: {frame_count}')

        # Clear the whole screen
        print(t.clear())

        # Print the player
        print(t.move(playerpos[1], playerpos[0]) + '@')

        # Handle input
        with t.cbreak():
            inp = t.inkey()

            # Escape key doesn't work and I don't know why.
            if inp in [t.KEY_ESCAPE, 'q']:
                logger.info('Quitting...')
                closed = True
                return True

            movediff = (0,0)
            if inp in "wk":
                movediff = (0,-1)
            elif inp in "sj":
                movediff = (0,1)
            elif inp in "ah":
                movediff = (-1,0)
            elif inp in "dl":
                movediff = (1,0)

        logger.debug('You pressed ' + repr(inp))
        logger.debug(playerpos)

        # Update player position
        playerpos = (
                playerpos[0] + movediff[0],
                playerpos[1] + movediff[1]
            )

        frame_count += 1

    print(t.exit_fullscreen())

if __name__ == '__main__':
    main()
