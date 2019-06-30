import logging

logger = logging.getLogger()

class BasicMonster:
    def take_turn(self):
        logger.info("The %s wonders when it will be able to move.", self.owner.name)
