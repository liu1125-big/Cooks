from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.models.user import User
from app.models.category import Category
from app.models.dish import Dish
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.auth import require_admin

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """创建分类（仅管理员）"""
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="分类名称已存在")
    
    try:
        db_category = Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="分类名称已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建分类失败: {str(e)}")


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """获取分类列表（公开）"""
    try:
        return db.query(Category).order_by(Category.sort, Category.id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分类列表失败: {str(e)}")


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """获取分类详情（公开）"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    return category


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int, 
    category: CategoryUpdate, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """更新分类（仅管理员）"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    if category.name is not None and category.name != db_category.name:
        existing = db.query(Category).filter(
            Category.name == category.name, 
            Category.id != category_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="分类名称已被其他分类使用")
    
    try:
        for key, value in category.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(db_category, key, value)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="分类名称已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新分类失败: {str(e)}")


@router.delete("/{category_id}")
def delete_category(
    category_id: int, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """删除分类（仅管理员）"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    related_dishes = db.query(Dish).filter(Dish.category_id == category_id).count()
    if related_dishes > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"该分类下有 {related_dishes} 个菜品，无法删除"
        )
    
    try:
        db.delete(db_category)
        db.commit()
        return {"message": "分类删除成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该分类有关联数据，无法删除")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除分类失败: {str(e)}")