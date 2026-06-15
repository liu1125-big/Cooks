import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.session import get_db
from app.models.user import User
from app.models.buy import Buy
from app.services.auth import get_current_user

router = APIRouter(prefix="/buy", tags=["buy"])


class BuyCreate(BaseModel):
    name: str
    price: float
    number: float
    date: datetime.date


class BuyUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    number: Optional[float] = None
    date: Optional[datetime.date] = None


class BuyResponse(BaseModel):
    id: int
    name: str
    price: float
    number: float
    date: datetime.date
    user_id: int
    user_name: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class BuyStatsResponse(BaseModel):
    total_amount: float
    total_count: int
    period: str


def is_admin(current_user: User) -> None:
    """检查是否为管理员"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足，需要管理员权限")


@router.post("", response_model=BuyResponse, status_code=201)
def create_buy(
    buy_data: BuyCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """新增采购记录（仅管理员）"""
    is_admin(current_user)

    buy_record = Buy(
        name=buy_data.name,
        price=buy_data.price,
        number=buy_data.number,
        date=buy_data.date,
        user_id=current_user.id
    )
    db.add(buy_record)
    db.commit()
    db.refresh(buy_record)
    buy_record.user_name = current_user.nickname
    return buy_record


@router.get("", response_model=list[BuyResponse])
def get_buy_list(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    name: Optional[str] = None,
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None
):
    """查询采购记录（仅管理员）"""
    is_admin(current_user)

    query = db.query(Buy, User.nickname.label('user_name')).join(
        User, Buy.user_id == User.id
    )

    # 按食材名称筛选
    if name:
        query = query.filter(Buy.name.like(f"%{name}%"))

    # 按采购日期筛选
    if start_date:
        query = query.filter(Buy.date >= start_date)
    if end_date:
        query = query.filter(Buy.date <= end_date)

    query = query.order_by(Buy.date.desc())
    items = query.all()

    result = []
    for item, user_name in items:
        item.user_name = user_name
        result.append(item)
    return result


@router.get("/{buy_id}", response_model=BuyResponse)
def get_buy_detail(
    buy_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """获取采购记录详情（仅管理员）"""
    is_admin(current_user)

    buy_record = db.query(Buy, User.nickname.label('user_name')).join(
        User, Buy.user_id == User.id
    ).filter(Buy.id == buy_id).first()

    if not buy_record:
        raise HTTPException(status_code=404, detail="采购记录不存在")

    buy_record[0].user_name = buy_record[1]
    return buy_record[0]


@router.put("/{buy_id}", response_model=BuyResponse)
def update_buy(
    buy_id: int,
    buy_data: BuyUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """修改采购记录（仅管理员）"""
    is_admin(current_user)

    buy_record = db.query(Buy).filter(Buy.id == buy_id).first()

    if not buy_record:
        raise HTTPException(status_code=404, detail="采购记录不存在")

    if buy_data.name is not None:
        buy_record.name = buy_data.name
    if buy_data.price is not None:
        buy_record.price = buy_data.price
    if buy_data.number is not None:
        buy_record.number = buy_data.number
    if buy_data.date is not None:
        buy_record.date = buy_data.date

    db.commit()
    db.refresh(buy_record)

    buy_record.user_name = current_user.nickname
    return buy_record


@router.delete("/{buy_id}", status_code=204)
def delete_buy(
    buy_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """删除采购记录（仅管理员）"""
    is_admin(current_user)

    buy_record = db.query(Buy).filter(Buy.id == buy_id).first()

    if not buy_record:
        raise HTTPException(status_code=404, detail="采购记录不存在")

    db.delete(buy_record)
    db.commit()
    return None


# 统计接口
@router.get("/stats/daily", response_model=BuyStatsResponse)
def get_daily_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    target_date: Optional[datetime.date] = None
):
    """日统计（仅管理员）"""
    is_admin(current_user)

    if target_date is None:
        target_date = datetime.date.today()

    stats = db.query(
        func.count(Buy.id).label('total_count'),
        func.sum(Buy.price * Buy.number).label('total_amount')
    ).filter(Buy.date == target_date).first()

    return BuyStatsResponse(
        total_amount=float(stats.total_amount or 0),
        total_count=stats.total_count or 0,
        period=f"{target_date}"
    )


@router.get("/stats/monthly", response_model=BuyStatsResponse)
def get_monthly_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db),
    year: Optional[int] = None,
    month: Optional[int] = None
):
    """月统计（仅管理员）"""
    is_admin(current_user)

    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month

    start_date = datetime.date(year, month, 1)
    if month == 12:
        end_date = datetime.date(year + 1, 1, 1)
    else:
        end_date = datetime.date(year, month + 1, 1)

    stats = db.query(
        func.count(Buy.id).label('total_count'),
        func.sum(Buy.price * Buy.number).label('total_amount')
    ).filter(Buy.date >= start_date, Buy.date < end_date).first()

    return BuyStatsResponse(
        total_amount=float(stats.total_amount or 0),
        total_count=stats.total_count or 0,
        period=f"{year}-{month:02d}"
    )