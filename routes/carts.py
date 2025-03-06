from fastapi import APIRouter, Depends, status
from auth import get_current_user
from crud.cart import add_drug_to_cart, empty_cart, get_cart_by_id, get_carts, remove_drug_from_cart
from database.session import get_db
from sqlalchemy.orm import Session

from models.user import User
from schemas.cart import Cart

router = APIRouter(
    prefix="/carts",
    tags=["Carts"]
)


@router.get("/", response_model=list[Cart])
def read_carts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_carts(skip, limit, db)

@router.get("/{cart_id}", response_model=Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    return get_cart_by_id(cart_id, db)

@router.post("/", response_model=Cart)
def get_cart_by_user_id(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_cart_by_user_id(current_user.id, db)

@router.post("/drugs", response_model=Cart)
def add_to_cart(drug_id: int, quantity: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_drug_to_cart(current_user.id, drug_id, quantity, db)

# @router.patch("/drugs/{drug_id}", response_model=Cart)
# def update_drug_in_cart(drug_id: int, quantity: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
#     return add_drug_to_cart(current_user.id, drug_id, quantity, db)

@router.delete("/drugs/{drug_id}")
def remove_from_cart(drug_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return remove_drug_from_cart(current_user.id, drug_id, db)

@router.delete("/")
def delete_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return empty_cart(current_user.id, db)