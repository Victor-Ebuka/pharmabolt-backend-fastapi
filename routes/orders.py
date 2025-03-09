from fastapi import APIRouter, Depends
from auth import get_current_user
from crud.orders import create_order_from_cart
from database.session import get_db
from models.order import Order
from models.user import User
from schemas.order import OrderCreate
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/from-cart/{user_id}")
def create_order(order_details: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    return create_order_from_cart(user_id, order_details, db)