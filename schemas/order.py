from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Annotated
from datetime import date

class OrderBase(BaseModel):
    status: Literal["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"]
    order_date: date
    delivery_date: Optional[date]
    payment_method: str
    delivery_method: str
    user_id: int
    product_total: int
    delivery_fee: int
    total_price: int
    delivery_address: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    order_no: int
    drugs: List["DrugOrder"]  # Added drugs to the order schema

    class Config:
        orm_mode = True

class DrugOrderBase(BaseModel):
    drug_id: int
    order_id: int
    quantity: Annotated[int, Field(ge=1)]  # Quantity should be at least 1

class DrugOrder(DrugOrderBase):
    id: int

    class Config:
        orm_mode = True

class UserOrder(BaseModel):
    id: int
    order_no: int
    drugs: List["DrugOrder"]