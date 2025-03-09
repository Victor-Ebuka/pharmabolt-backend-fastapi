from sqlalchemy.orm import Session
from models.drug import Drug
from models.user import User
from fastapi import HTTPException
from models.cart import Cart
from models.drug_cart import DrugCart

def retrieve_cart_by_user_id(user_id: int, db: Session) -> Cart:
    # cart = db.query(Cart).filter(Cart.user_id == user_id).join(DrugCart, DrugCart.cart_id == Cart.id).first()
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

def get_cart_by_id(cart_id: int, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.id == cart_id).join(DrugCart, DrugCart.cart_id == Cart.id).join(User, User.id == Cart.user_id).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart

def add_drug_to_cart(user_id: int, drug_id: int, quantity: int, db: Session) -> Cart:
    # Check if the user has an existing cart, if not create one
    cart = retrieve_cart_by_user_id(user_id, db)
    if not cart:
        cart = Cart(user_id=user_id, total_price=0)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    # Fetch the drug
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    
    # Ensure there is enough stock
    if drug.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Check if drug already exists in the cart
    drug_cart = db.query(DrugCart).filter(
        DrugCart.cart_id == cart.id, DrugCart.drug_id == drug_id
    ).first()

    if drug_cart:
        # Update the quantity
        drug_cart.quantity += quantity
    else:
        # Add new entry
        drug_cart = DrugCart(cart_id=cart.id, drug_id=drug_id, quantity=quantity)
        db.add(drug_cart)

    # Update total price
    cart.total_price += drug.price * quantity

    # Commit the changes
    db.commit()
    db.refresh(cart)

    return cart
    
def remove_drug_from_cart(user_id: int, drug_id: int, db: Session) -> Cart:
    cart = retrieve_cart_by_user_id(user_id, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    drug_cart = db.query(DrugCart).filter(
        DrugCart.cart_id == cart.id, DrugCart.drug_id == drug_id
    ).first()

    if not drug_cart:
        raise HTTPException(status_code=404, detail="Drug not found in cart")

    # Reduce total price before removing the drug
    cart.total_price -= drug_cart.quantity * db.query(Drug).filter(Drug.id == drug_id).first().price

    # Remove the drug from the cart
    db.delete(drug_cart)
    db.commit()
    db.refresh(cart)

    return cart

def empty_cart(user_id: int, db: Session) -> Cart:
    cart = retrieve_cart_by_user_id(user_id, db)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Remove all drugs from the cart
    db.query(DrugCart).filter(DrugCart.cart_id == cart.id).delete()

    # Reset total price
    cart.total_price = 0

    db.commit()
    db.refresh(cart)

    return cart
