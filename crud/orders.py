from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from models.cart import Cart 
from models.order import Order
from models.drug_order import DrugOrder
from models.drug_cart import DrugCart
from schemas.order import OrderCreate, DrugOrderBase
from database.session import get_db  # Assuming a db session function


def create_order_from_cart(user_id: int, order_details: OrderCreate, db: Session = Depends(get_db)):
    cart_query = db.query(Cart).filter(Cart.user_id == user_id)
    # 1. Fetch the user's cart
    db_cart = cart_query.first()
    if not db_cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # 2. Ensure the cart is not empty
    cart_with_drugs = cart_query.join(DrugCart, DrugCart.cart_id == Cart.id).first()
    if not cart_with_drugs.drugs:
        raise HTTPException(status_code=404, detail="Cart is empty")

    # Calculate totals
    for drug in cart_with_drugs.drugs:
        order_details.product_total += drug.quantity
        
    order_details.delivery_fee = 500  # Example fee, adjust as needed
    order_details.total_price = order_details.product_total + order_details.delivery_fee

    # 3. Create Order
    new_order = Order(
        order_date=order_details.order_date,
        delivery_date=None,
        payment_method=order_details.payment_method,  
        delivery_method=order_details.delivery_method,
        user_id=user_id,
        product_total=order_details.product_total,
        delivery_fee=order_details.delivery_fee,
        total_price=order_details.total_price,
        delivery_address=order_details.delivery_address  # Should come from user's saved addresses
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # 4. Move drugs from Cart to Order
    for cart_item in cart_with_drugs.drugs:
        new_drug_order = DrugOrder(
            drug_id=cart_item.drug_id,
            order_id=new_order.id,
            quantity=cart_item.quantity
        )
        db.add(new_drug_order)

    db.commit()

    # 5. Clear the cart
    db.query(DrugCart).filter(DrugCart.cart_id == db_cart.id).delete()
    db.commit()

    return new_order
