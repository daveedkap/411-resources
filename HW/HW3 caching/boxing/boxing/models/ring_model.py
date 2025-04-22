import logging
import math
import os
import time
from typing import List

from boxing.models.boxers_model import Boxers
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random

logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """A class to manage the ring in which boxers have fights."""

    def __init__(self):
        self.ring: List[int] = []
        self._boxer_cache: dict[int, Boxers] = {}
        self._ttl: dict[int, float] = {}
        self.ttl_seconds = int(os.getenv("TTL_SECONDS", 60))

    def fight(self) -> str:
        if len(self.ring) < 2:
            logger.error("There must be two boxers to start a fight.")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()
        logger.info(f"Fight started between {boxer_1.name} and {boxer_2.name}")

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)

        logger.debug(f"Fighting skill for {boxer_1.name}: {skill_1:.3f}")
        logger.debug(f"Fighting skill for {boxer_2.name}: {skill_2:.3f}")

        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        logger.debug(f"Raw delta between skills: {delta:.3f}")
        logger.debug(f"Normalized delta: {normalized_delta:.3f}")

        random_number = get_random()
        logger.debug(f"Random number from random.org: {random_number:.3f}")

        if random_number < normalized_delta:
            winner, loser = boxer_1, boxer_2
        else:
            winner, loser = boxer_2, boxer_1

        logger.info(f"The winner is: {winner.name}")
        winner.update_stats("win")
        loser.update_stats("loss")
        self.clear_ring()
        return winner.name

    def clear_ring(self):
        if not self.ring:
            logger.warning("Attempted to clear an empty ring.")
            return
        logger.info("Clearing the boxers from the ring.")
        self.ring.clear()

    def enter_ring(self, boxer_id: int):
        if len(self.ring) >= 2:
            logger.error(f"Attempted to add boxer ID {boxer_id} but the ring is full")
            raise ValueError("Ring is full")

        try:
            boxer = Boxers.get_boxer_by_id(boxer_id)
        except ValueError as e:
            logger.error(str(e))
            raise

        logger.info(f"Adding boxer '{boxer.name}' (ID {boxer_id}) to the ring")
        self.ring.append(boxer_id)
        logger.info(f"Current boxers in the ring: {[Boxers.get_boxer_by_id(b).name for b in self.ring]}")

    def get_boxers(self) -> List[Boxers]:
        if not self.ring:
            logger.warning("Retrieving boxers from an empty ring.")
            return []

        logger.info(f"Retrieving {len(self.ring)} boxers from the ring.")
        boxers: List[Boxers] = []

        for boxer_id in self.ring:
            ttl = self._ttl.get(boxer_id)
            expired = ttl is None or time.time() > ttl

            if expired:
                logger.info(f"TTL expired or missing for boxer {boxer_id}. Refreshing from DB.")
                boxer = Boxers.get_boxer_by_id(boxer_id)
                self._boxer_cache[boxer_id] = boxer
                self._ttl[boxer_id] = time.time() + self.ttl_seconds
            else:
                logger.debug(f"Using cached boxer {boxer_id} (TTL valid).")
                boxer = self._boxer_cache[boxer_id]

            boxers.append(boxer)

        logger.info(f"Retrieved {len(boxers)} boxers from the ring.")
        return boxers

    def get_fighting_skill(self, boxer: Boxers) -> float:
        logger.info(f"Calculating fighting skill for {boxer.name}: weight={boxer.weight}, age={boxer.age}, reach={boxer.reach}")
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier
        logger.info(f"Fighting skill for {boxer.name}: {skill:.3f}")
        return skill

    def clear_cache(self):
        logger.info("Clearing local boxer cache in RingModel.")
        self._boxer_cache.clear()
        self._ttl.clear()
