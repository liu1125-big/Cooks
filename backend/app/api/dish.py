from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.dish import Dish
from app.schemas.dish import DishCreate, DishUpdate, DishResponse

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.post("", response_model=DishResponse)
def create_dish(dish: DishCreate, db: Session = Depends(get_db)):
    db_dish = Dish(**dish.model_dump())
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.get("", response_model=list[DishResponse])
def get_dishes(
    keyword: str | None = None,
    category_id: int | None = None,
    favorite: bool | None = None,
    difficulty: int | None = None,
    enabled: bool | None = None,
    db: Session = Depends(get_db)
):
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
    return query.all()


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@router.put("/{dish_id}", response_model=DishResponse)
def update_dish(dish_id: int, dish: DishUpdate, db: Session = Depends(get_db)):
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    for key, value in dish.model_dump(exclude_unset=True).items():
        setattr(db_dish, key, value)
    db.commit()
    db.refresh(db_dish)
    return db_dish


@router.delete("/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    db_dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if not db_dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(db_dish)
    db.commit()
    return {"message": "Dish deleted successfully"}