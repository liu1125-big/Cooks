from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.dish import Dish
from app.models.history import History


class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def get_random_dish(self, category_id: int | None = None, exclude_days: int | None = None):
        query = self.db.query(Dish).filter(Dish.enabled == True)

        if category_id is not None:
            query = query.filter(Dish.category_id == category_id)

        if exclude_days is not None and exclude_days > 0:
            cutoff_date = datetime.now() - timedelta(days=exclude_days)
            recent_dish_ids = (
                self.db.query(History.dish_id)
                .filter(History.created_at >= cutoff_date)
                .distinct()
                .all()
            )
            recent_ids = [dish_id for (dish_id,) in recent_dish_ids]
            if recent_ids:
                query = query.filter(~Dish.id.in_(recent_ids))

        return query.first()