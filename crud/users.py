from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from auth import hash_password
from models.cart import Cart
from models.order import Order
from models.prescription import Prescription
from models.user import User
from fastapi import HTTPException
from schemas.user import UserCreate, UserUpdate


def get_users(skip: int, limit: int, db: Session) -> list[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    return users

def get_users_with_details(skip: int, limit: int, db: Session) -> list[User]:
    pass

def add_user(new_user: UserCreate, db: Session) -> User:
    db_user = db.query(User).filter(func.lower(User.email) == new_user.email.lower()).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = db.query(User).filter(func.lower(User.phone_no) == new_user.phone_no.lower()).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    new_user_data = new_user.model_dump()
    new_user_data["password"] = hash_password(new_user.password)  # Hash the password
    new_user = User(**new_user_data)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    user_cart = Cart(user_id=new_user.id, total_price=0)
    db.add(user_cart)
    db.commit()

    return new_user

def get_user_profile(user: User, db: Session) -> User:
    db_orders = db.query(Order).filter(Order.user_id == user.id).all()
    db_cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    db_prescriptions = db.query(Prescription).filter(Prescription.user_id == user.id).all()

    return {
        "user": user,
        "orders": db_orders,
        "cart": db_cart,
        "prescriptions": db_prescriptions
    }

def get_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_phone_no_and_email(phone_no: str, email: str, db: Session) -> User:
    query = db.query(User)

    if email:
        query = query.filter(func.lower(User.email).ilike(f"%{email.lower()}%"))

    if phone_no:
        query = query.filter(User.phone_no.ilike(f"%{phone_no}%"))

    user = query.first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def get_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(func.lower(User.email).like(f"%{email.lower()}%")).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def get_user_by_phone_no(phone_no: str, db: Session) -> User:
    user = db.query(User).filter(func.lower(User.phone_no).like(f"%{phone_no.lower()}%")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(user_id: int, db: Session):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return True

def update_user(user: UserUpdate, current_user: User, db: Session):
    if db.query(User).filter(User.phone_no == user.phone_no):
        raise HTTPException(status_code=400, detail=f"User with phone number {user.phone_no} exists")
    for key, value in user.model_dump().items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return get_user_profile(current_user, db)