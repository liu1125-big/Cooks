from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.history import History
from app.schemas.history import HistoryCreate, HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.post("", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    db_history = History(**history.model_dump())
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


@router.get("", response_model=list[HistoryResponse])
def get_history(
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    dish_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(History)
    if start_date:
        query = query.filter(History.created_at >= start_date)
    if end_date:
        query = query.filter(History.created_at <= end_date)
    if dish_id is not None:
        query = query.filter(History.dish_id == dish_id)
    return query.order_by(History.created_at.desc()).all()


@router.get("/{history_id}", response_model=HistoryResponse)
def get_history_item(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    return history


@router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="History not found")
    db.delete(history)
    db.commit()
    return {"message": "History deleted successfully"}