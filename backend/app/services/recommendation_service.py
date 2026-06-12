import random
from sqlalchemy.orm import Session
from app.models.dish import Dish


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def get_random_dish(self, category: str | None = None):
        query = self.db.query(Dish)

        if category is not None:
            query = query.filter(Dish.category == category)

        # Get all matching dishes and pick a random one
        all_dishes = query.all()
        if not all_dishes:
            return None
        return random.choice(all_dishes)