from sqlalchemy.orm import Session
from models.cart import Cart
from models.user import User
from fastapi import HTTPException
from schemas.user import UserCreate


def get_users(skip: int, limit: int, db: Session) -> list[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_users_with_details(skip: int, limit: int, db: Session) -> list[User]:
    pass

def add_user(new_user: UserCreate, db: Session) -> User:
    db_user = db.query(User).filter(User.email.lower() == new_user.email.lower()).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = db.query(User).filter(User.phone_no.lower() == new_user.phone_no.lower()).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    new_user = User(**new_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    user_cart = Cart(user_id=new_user.id)
    db.add(user_cart)
    db.commit()
    return new_user

def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
