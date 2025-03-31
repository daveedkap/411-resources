import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random

logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    def __init__(self):
        self.ring: List[Boxer] = []
        logger.info("Initialized RingModel with an empty ring.")

    def fight(self) -> str:
        logger.info("Fight initiated.")
        if len(self.ring) < 2:
            logger.error("Fight cannot start: less than 2 boxers in the ring.")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()
        logger.info(f"Boxers selected for fight: {boxer_1.name} and {boxer_2.name}")

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)
        logger.info(f"Calculated fighting skills - {boxer_1.name}: {skill_1}, {boxer_2.name}: {skill_2}")

        # Compute the absolute skill difference and normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))
        logger.info(f"Skill difference: {delta}, normalized delta: {normalized_delta}")

        random_number = get_random()
        logger.info(f"Random number generated: {random_number}")

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        logger.info(f"Fight result determined: Winner - {winner.name}, Loser - {loser.name}")

        logger.info("Updating boxer stats for the fight outcome.")
        update_boxer_stats(winner.id, 'win')
        update_boxer_stats(loser.id, 'loss')
        logger.info("Boxer stats updated successfully.")

        logger.info("Clearing ring after fight.")
        self.clear_ring()

        logger.info(f"Fight completed. Winner is {winner.name}")
        return winner.name

    def clear_ring(self):
        if not self.ring:
            logger.info("Clear ring requested but the ring is already empty.")
            return
        self.ring.clear()
        logger.info("Ring cleared successfully.")

    def enter_ring(self, boxer: Boxer):
        logger.info(f"Attempting to add boxer '{boxer.name}' to the ring.")
        if not isinstance(boxer, Boxer):
            logger.error(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")
            raise TypeError(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")

        if len(self.ring) >= 2:
            logger.warning("Ring is full, cannot add more boxers.")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Boxer '{boxer.name}' entered the ring. Current ring size: {len(self.ring)}")

    def get_boxers(self) -> List[Boxer]:
        logger.info("Retrieving current boxers in the ring.")
        logger.info(f"Current ring contains {len(self.ring)} boxer(s).")
        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        logger.info(f"Calculating fighting skill for boxer '{boxer.name}'.")
        # Arbitrary calculations:
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier
        logger.info(f"Fighting skill for boxer '{boxer.name}' calculated as {skill}.")
        return skill