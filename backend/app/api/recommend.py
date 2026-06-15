from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.recommendation_service import RecommendationService
from app.schemas.recommend import RecommendDishResponse

router = APIRouter(prefix="", tags=["recommend"])


@router.get("/random", response_model=RecommendDishResponse)
def get_random_recommendation(
    category: str | None = None,
    db: Session = Depends(get_db)
):
    service = RecommendationService(db)
    dish = service.get_random_dish(category=category)
    if not dish:
        raise HTTPException(status_code=404, detail="没有符合条件的菜品")
    return dish