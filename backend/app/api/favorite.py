from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.dish import Dish
from app.models.favorite import Favorite
from app.services.auth import get_current_user

router = APIRouter(prefix="/favorites", tags=["favorites"])


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    dish_id: int
    dish_name: str | None = None
    category_name: str | None = None
    created_at: datetime | None = None

    class Config:
        from_attributes = True


@router.post("/{dish_id}", status_code=201)
def add_favorite(
    dish_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """添加收藏"""
    # 检查菜品是否存在
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在")

    # 检查是否已收藏
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.dish_id == dish_id
    ).first()

    if existing:
        return {"message": "已收藏", "dish_id": dish_id}

    # 添加收藏
    favorite = Favorite(user_id=current_user.id, dish_id=dish_id)
    db.add(favorite)
    db.commit()
    return {"message": "收藏成功", "dish_id": dish_id}


@router.delete("/{dish_id}", status_code=204)
def remove_favorite(
    dish_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """取消收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.dish_id == dish_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="收藏不存在")

    db.delete(favorite)
    db.commit()
    return None


@router.get("", response_model=list[FavoriteResponse])
def get_favorites(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """获取当前用户的收藏列表"""
    items = db.query(Favorite, Dish.name.label('dish_name')).join(
        Dish, Favorite.dish_id == Dish.id
    ).filter(Favorite.user_id == current_user.id).all()

    result = []
    for item, dish_name in items:
        item.dish_name = dish_name
        result.append(item)
    return result


@router.get("/{dish_id}", response_model=FavoriteResponse)
def check_favorite(
    dish_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """检查菜品是否已收藏"""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.dish_id == dish_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="未收藏")

    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    favorite.dish_name = dish.name if dish else None
    return favorite