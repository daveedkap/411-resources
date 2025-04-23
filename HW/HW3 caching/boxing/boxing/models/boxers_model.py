import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from boxing.db import db
from boxing.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

class Boxers(db.Model):
    __tablename__ = "boxers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    reach = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    fights = db.Column(db.Integer, nullable=False, default=0)
    wins = db.Column(db.Integer, nullable=False, default=0)
    weight_class = db.Column(db.String)

    def __init__(self, name: str, weight: float, height: float, reach: float, age: int):
        if weight < 125:
            raise ValueError("Weight must be at least 125 lbs.")
        if height <= 0:
            raise ValueError("Height must be greater than 0.")
        if reach <= 0:
            raise ValueError("Reach must be greater than 0.")
        if not (18 <= age <= 40):
            raise ValueError("Age must be between 18 and 40.")

        self.name = name
        self.weight = weight
        self.height = height
        self.reach = reach
        self.age = age
        self.weight_class = self.get_weight_class(weight)
        self.fights = 0
        self.wins = 0

    @classmethod
    def get_weight_class(cls, weight: float) -> str:
        if weight < 125:
            raise ValueError("Invalid weight for boxing.")
        elif weight < 135:
            return "Lightweight"
        elif weight < 147:
            return "Welterweight"
        elif weight < 160:
            return "Middleweight"
        elif weight < 175:
            return "Light Heavyweight"
        else:
            return "Heavyweight"

    @classmethod
    def create_boxer(cls, name: str, weight: float, height: float, reach: float, age: int) -> None:
        logger.info(f"Creating boxer: {name}, {weight=} {height=} {reach=} {age=}")
        try:
            boxer = cls(name, weight, height, reach, age)
            db.session.add(boxer)
            db.session.commit()
            logger.info(f"Boxer created successfully: {name}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Boxer with name '{name}' already exists.")
            raise ValueError(f"Boxer with name '{name}' already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise

    @classmethod
    def get_boxer_by_id(cls, boxer_id: int) -> "Boxers":
        boxer = db.session.get(cls, boxer_id)
        if boxer is None:
            logger.info(f"Boxer with ID {boxer_id} not found.")
            raise ValueError(f"Boxer with ID {boxer_id} not found.")
        return boxer

    @classmethod
    def get_boxer_by_name(cls, name: str) -> "Boxers":
        boxer = cls.query.filter_by(name=name).first()
        if boxer is None:
            logger.info(f"Boxer '{name}' not found.")
            raise ValueError(f"Boxer '{name}' not found.")
        return boxer

    @classmethod
    def delete(cls, boxer_id: int) -> None:
        boxer = cls.get_boxer_by_id(boxer_id)
        db.session.delete(boxer)
        db.session.commit()
        logger.info(f"Boxer with ID {boxer_id} permanently deleted.")

    def update_stats(self, result: str) -> None:
        if result not in {"win", "loss"}:
            raise ValueError("Result must be 'win' or 'loss'.")

        self.fights += 1
        if result == "win":
            self.wins += 1

        if self.wins > self.fights:
            raise ValueError("Wins cannot exceed number of fights.")

        db.session.commit()
        logger.info(f"Updated stats for boxer {self.name}: {self.fights} fights, {self.wins} wins.")

    @staticmethod
    def get_leaderboard(sort_by: str = "wins") -> List[dict]:
        logger.info(f"Retrieving leaderboard. Sort by: {sort_by}")
        if sort_by not in {"wins", "win_pct"}:
            logger.error(f"Invalid sort_by parameter: {sort_by}")
            raise ValueError(f"Invalid sort_by parameter: {sort_by}")

        boxers = Boxers.query.filter(Boxers.fights > 0).all()

        def compute_win_pct(b: Boxers) -> float:
            return round((b.wins / b.fights) * 100, 1) if b.fights > 0 else 0.0

        leaderboard = [{
            "id": b.id,
            "name": b.name,
            "weight": b.weight,
            "height": b.height,
            "reach": b.reach,
            "age": b.age,
            "weight_class": b.weight_class,
            "fights": b.fights,
            "wins": b.wins,
            "win_pct": compute_win_pct(b)
        } for b in boxers]

        leaderboard.sort(key=lambda b: b[sort_by], reverse=True)
        logger.info("Leaderboard retrieved successfully.")
        return leaderboard
