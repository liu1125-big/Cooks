from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.models.user import User
from app.models.history import History
from app.models.dish import Dish
from app.schemas.history import HistoryCreate, HistoryResponse
from app.services.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("", response_model=HistoryResponse, status_code=201)
def create_history(
    history: HistoryCreate, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """创建历史记录（登录用户）"""
    dish = db.query(Dish).filter(Dish.id == history.dish_id).first()
    if not dish:
        raise HTTPException(status_code=400, detail="指定的菜品不存在")
    
    if history.selected_by is None:
        history.selected_by = current_user.id
    
    try:
        db_history = History(**history.model_dump())
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        return db_history
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="创建历史记录失败")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"创建历史记录失败: {str(e)}")


@router.get("", response_model=list[HistoryResponse])
def get_history(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    dish_id: int | None = None,
    selected_by: int | None = None,
    selected_method: str | None = None,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(50, ge=1, le=500, description="返回记录数"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: Session = Depends(get_db)
):
    """获取历史记录"""
    try:
        query = db.query(History)
        
        if current_user.role != "admin":
            if selected_by is None:
                selected_by = current_user.id
            elif selected_by != current_user.id:
                raise HTTPException(status_code=403, detail="只能查看自己的历史记录")
        
        if start_date:
            query = query.filter(History.created_at >= start_date)
        if end_date:
            query = query.filter(History.created_at <= end_date)
        if dish_id is not None:
            query = query.filter(History.dish_id == dish_id)
        if selected_by is not None:
            query = query.filter(History.selected_by == selected_by)
        if selected_method is not None:
            query = query.filter(History.selected_method == selected_method)
        
        return query.order_by(History.created_at.desc()).offset(skip).limit(limit).all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@router.get("/{history_id}", response_model=HistoryResponse)
def get_history_item(
    history_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """获取单条历史记录"""
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    
    if current_user.role != "admin" and history.selected_by != current_user.id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    return history


@router.delete("/{history_id}")
def delete_history(
    history_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """删除历史记录"""
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="历史记录不存在")
    
    if current_user.role != "admin" and history.selected_by != current_user.id:
        raise HTTPException(status_code=403, detail="只能删除自己的历史记录")
    
    try:
        db.delete(history)
        db.commit()
        return {"message": "历史记录删除成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="删除历史记录失败")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除历史记录失败: {str(e)}")


@router.delete("")
def clear_history(
    current_user: Annotated[User, Depends(require_admin)],
    dish_id: int | None = None,
    selected_by: int | None = None,
    days: int | None = None,
    db: Session = Depends(get_db)
):
    """批量删除历史记录（仅管理员）"""
    try:
        query = db.query(History)
        
        if dish_id is not None:
            query = query.filter(History.dish_id == dish_id)
        if selected_by is not None:
            query = query.filter(History.selected_by == selected_by)
        if days is not None:
            cutoff_date = datetime.now() - timedelta(days=days)
            query = query.filter(History.created_at < cutoff_date)
        
        deleted_count = query.delete()
        db.commit()
        return {"message": f"成功删除 {deleted_count} 条历史记录"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"批量删除历史记录失败: {str(e)}")