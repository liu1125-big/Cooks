from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.dish import Dish
from app.models.cart import Cart
from app.services.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


class CartItemCreate(BaseModel):
    dish_id: int


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    dish_id: int
    dish_name: str | None = None

    class Config:
        from_attributes = True


@router.post("", response_model=CartItemResponse, status_code=201)
def add_to_cart(
    item: CartItemCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """添加菜品到购物车"""
    # 检查菜品是否存在
    dish = db.query(Dish).filter(Dish.id == item.dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在")

    # 检查是否已在购物车中
    existing = db.query(Cart).filter(
        Cart.user_id == current_user.id,
        Cart.dish_id == item.dish_id
    ).first()

    if existing:
        # 该菜品已在购物车中，请勿重复添加
        raise HTTPException(status_code=400, detail="该菜品已在购物车中，请勿重复添加")

    # 新增购物车项
    cart_item = Cart(user_id=current_user.id, dish_id=item.dish_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    cart_item.dish_name = dish.name
    return cart_item


@router.get("", response_model=list[CartItemResponse])
def get_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """获取当前用户的购物车"""
    items = db.query(Cart, Dish.name.label('dish_name')).join(
        Dish, Cart.dish_id == Dish.id
    ).filter(Cart.user_id == current_user.id).all()

    result = []
    for item, dish_name in items:
        item.dish_name = dish_name
        result.append(item)
    return result


@router.delete("/{item_id}", status_code=204)
def remove_from_cart(
    item_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """从购物车移除菜品"""
    cart_item = db.query(Cart).filter(
        Cart.id == item_id,
        Cart.user_id == current_user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="购物车项不存在")

    db.delete(cart_item)
    db.commit()
    return None


@router.delete("", status_code=204)
def clear_cart(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """清空购物车"""
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()
    return None