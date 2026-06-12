from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.models.user import User
from app.models.dish import Dish
from app.models.category import Category
from app.models.history import History
from app.schemas.dish import DishCreate, DishUpdate, DishResponse
from app.services.auth import get_current_user, require_admin

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.post("", response_model=DishResponse, status_code=201)
def create_dish(
    dish: DishCreate, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """创建菜品（仅管理员）"""
    if dish.category_id:
        category = db.query(Category).filter(Category.id == dish.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="指定的分类不存在")
    
    existing = db.query(Dish).filter(Dish.name == dish.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="菜品名称已存在")
    
    try:
        db_dish = Dish(**dish.model_dump())
        db.add(db_dish)
        db.commit()
        db.refresh(db_dish)
        return db_dish
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="菜品名称已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建菜品失败: {str(e)}")


@router.get("", response_model=list[DishResponse])
def get_dishes(
    keyword: str | None = None,
    category_id: int | None = None,
    favorite: bool | None = None,
    difficulty: int | None = None,
    enabled: bool | None = None,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数"),
    db: Session = Depends(get_db)
):
    """获取菜品列表（公开）"""
    try:
        query = db.query(Dish)
        
        if keyword:
            query = query.filter(Dish.name.contains(keyword))
        if category_id is not None:
            query = query.filter(Dish.category_id == category_id)
        if favorite is not None:
            query = query.filter(Dish.favorite == favorite)
        if difficulty is not None:
            query = query.filter(Dish.difficulty == difficulty)
        if enabled is not None:
            query = query.filter(Dish.enabled == enabled)
        
        return query.order_by(Dish.id).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取菜品列表失败: {str(e)}")


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    """获取菜品详情（公开）"""
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    return dish


@router.put("/{dish_id}", response_model=DishResponse)
def update_dish(
    dish_id: int, 
    dish: DishUpdate, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """更新菜品（仅管理员）"""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    
    if dish.category_id is not None:
        category = db.query(Category).filter(Category.id == dish.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="指定的分类不存在")
    
    if dish.name is not None and dish.name != db_dish.name:
        existing = db.query(Dish).filter(
            Dish.name == dish.name, 
            Dish.id != dish_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="菜品名称已被其他菜品使用")
    
    try:
        for key, value in dish.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(db_dish, key, value)
        db.commit()
        db.refresh(db_dish)
        return db_dish
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="菜品名称已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新菜品失败: {str(e)}")


@router.delete("/{dish_id}")
def delete_dish(
    dish_id: int, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """删除菜品（仅管理员）"""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    
    related_history = db.query(History).filter(History.dish_id == dish_id).count()
    if related_history > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"该菜品有 {related_history} 条历史记录，无法删除"
        )
    
    try:
        db.delete(db_dish)
        db.commit()
        return {"message": "菜品删除成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该菜品有关联数据，无法删除")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除菜品失败: {str(e)}")


@router.post("/{dish_id}/favorite")
def toggle_favorite(
    dish_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """切换菜品收藏状态（登录用户）"""
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="菜品不存在")
    
    try:
        db_dish.favorite = not db_dish.favorite
        db.commit()
        db.refresh(db_dish)
        return {"message": "收藏状态已更新", "favorite": db_dish.favorite}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新收藏状态失败: {str(e)}")