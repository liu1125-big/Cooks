from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.user import User
from app.models.dish import Dish
from app.models.cart import Cart
from app.models.history import History
from app.services.auth import get_current_user

router = APIRouter(prefix="/history", tags=["history"])


class HistoryResponse(BaseModel):
    id: int
    user_id: int
    dish_id: int
    dish_name: Optional[str] = None
    category: Optional[str] = None
    time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    message: str
    order_id: Optional[str] = None
    total_count: int


@router.post("/submit", response_model=OrderResponse, status_code=201)
def submit_order(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """提交订单：将购物车中的菜品写入历史记录"""
    # 获取购物车中的所有菜品
    cart_items = db.query(Cart).filter(Cart.user_id == current_user.id).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="购物车为空，无法提交订单")

    # 获取当前时间作为下单时间
    order_time = datetime.now()

    # 将每道菜生成一条历史记录
    for item in cart_items:
        history_record = History(
            user_id=current_user.id,
            dish_id=item.dish_id,
            time=order_time
        )
        db.add(history_record)

    db.commit()

    # 清空购物车
    db.query(Cart).filter(Cart.user_id == current_user.id).delete()
    db.commit()

    return OrderResponse(
        message="订单提交成功",
        order_id=f"ORD{order_time.strftime('%Y%m%d%H%M%S')}",
        total_count=len(cart_items)
    )


@router.get("", response_model=list[HistoryResponse])
def get_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """获取历史订单列表（支持按时间筛选）"""
    query = db.query(History, Dish.name.label('dish_name')).join(
        Dish, History.dish_id == Dish.id
    ).filter(History.user_id == current_user.id)

    # 按时间筛选
    if start_date:
        query = query.filter(History.time >= start_date)
    if end_date:
        query = query.filter(History.time <= end_date)

    # 按时间倒序
    query = query.order_by(History.time.desc())

    items = query.all()

    result = []
    for item, dish_name in items:
        item.dish_name = dish_name
        result.append(item)
    return result


@router.delete("/{history_id}", status_code=204)
def delete_history(
    history_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """删除历史记录"""
    history_record = db.query(History).filter(
        History.id == history_id,
        History.user_id == current_user.id
    ).first()

    if not history_record:
        raise HTTPException(status_code=404, detail="历史记录不存在")

    db.delete(history_record)
    db.commit()
    return None


@router.delete("", status_code=204)
def clear_history(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """清空历史记录"""
    db.query(History).filter(History.user_id == current_user.id).delete()
    db.commit()
    return None