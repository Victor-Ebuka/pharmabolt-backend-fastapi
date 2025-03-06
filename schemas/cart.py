from pydantic import BaseModel
from typing import Optional, List, Annotated
from pydantic import Field

class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class CartUpdate(BaseModel):
    user_id: Optional[int] = None

class Cart(CartBase):
    id: int
    drugs: Optional[List["DrugCart"]]  # Updated to include drugs in the cart

    class Config:
        from_attributes = True

class DrugCartBase(BaseModel):
    cart_id: int
    drug_id: int
    quantity: Annotated[int, Field(ge=1)]  # Must be at least 1

class DrugCart(DrugCartBase):
    id: int

    class Config:
        from_attributes = True
