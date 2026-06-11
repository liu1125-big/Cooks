from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.recommendation_service import RecommendationService
from app.schemas.recommend import RecommendDishResponse

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/random", response_model=RecommendDishResponse)
def get_random_recommendation(
    category_id: int | None = None,
    exclude_days: int | None = Query(default=None, ge=0),
    db: Session = Depends(get_db)
):
    service = RecommendationService(db)
    dish = service.get_random_dish(category_id=category_id, exclude_days=exclude_days)
    if not dish:
        raise HTTPException(status_code=404, detail="No dish found matching criteria")
    return dish