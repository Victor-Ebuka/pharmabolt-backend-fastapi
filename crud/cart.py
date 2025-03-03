from sqlalchemy.orm import Session
from models.user import User
from fastapi import HTTPException
from models.cart import Cart
from models.drug_cart import DrugCart

def get_cart_by_user_id(user_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def get_carts(skip: int, limit: int, db: Session) -> list[Cart]:
    carts = db.query(Cart).offset(skip).limit(limit).all()
    return carts

def get_carts_by_drug_id(drug_id: int, db: Session) -> list[Cart]:
    carts = db.query(Cart).join(DrugCart, DrugCart.cart_id == Cart.id).filter(DrugCart.drug_id == drug_id).all()
    return carts