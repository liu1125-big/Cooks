import random
from sqlalchemy.orm import Session
from app.models.dish import Dish


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def get_random_dish(self, category_id: int | None = None):
        query = self.db.query(Dish).filter(Dish.enabled == True)

        if category_id is not None:
            query = query.filter(Dish.category_id == category_id)

        # Get all matching dishes and pick a random one
        all_dishes = query.all()
        if not all_dishes:
            return None
        return random.choice(all_dishes)