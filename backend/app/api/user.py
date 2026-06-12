from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse, LoginRequest, Token
from app.services.auth import (
    authenticate_user, 
    create_access_token, 
    get_current_user, 
    require_admin,
    get_password_hash
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    if user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="无效的角色")
    
    try:
        db_user = User(
            username=user.username,
            password_hash=get_password_hash(user.password),
            nickname=user.nickname,
            role=user.role
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="用户名已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")


@router.post("/login", response_model=Token)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录"""
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("", response_model=list[UserResponse])
def get_users(
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """获取用户列表（仅管理员）"""
    try:
        return db.query(User).order_by(User.id).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户列表失败: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int, 
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    """获取指定用户"""
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """更新用户（仅管理员）"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.username is not None and user.username != db_user.username:
        existing_user = db.query(User).filter(
            User.username == user.username, 
            User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已被其他用户使用")
    
    if user.role is not None and user.role not in ["admin", "user"]:
        raise HTTPException(status_code=400, detail="无效的角色")
    
    try:
        for key, value in user.model_dump(exclude_unset=True).items():
            if value is not None:
                if key == "password":
                    setattr(db_user, "password_hash", get_password_hash(value))
                else:
                    setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="用户名已存在")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"更新用户失败: {str(e)}")


@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    current_user: Annotated[User, Depends(require_admin)],
    db: Session = Depends(get_db)
):
    """删除用户（仅管理员）"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    
    try:
        db.delete(db_user)
        db.commit()
        return {"message": "用户删除成功"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该用户有关联数据，无法删除")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除用户失败: {str(e)}")