from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Annotated
from datetime import date

class OrderBase(BaseModel):
    status: Literal["PENDING", "SHIPPED", "DELIVERED", "CANCELLED"] = "PENDING"
    order_date: date
    payment_method: str
    delivery_method: str
    product_total: int
    delivery_address: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    user_id: int
    order_no: int
    total_price: int
    delivery_fee: int
    delivery_date: Optional[date]
    drugs: List["DrugOrder"]  # Added drugs to the order schema

    class Config:
        from_attributes = True

class DrugOrderBase(BaseModel):
    drug_id: int
    order_id: int
    quantity: Annotated[int, Field(ge=1)]  # Quantity should be at least 1

class DrugOrder(DrugOrderBase):
    id: int

    class Config:
        from_attributes = True

class UserOrder(BaseModel):
    id: int
    order_no: int
    drugs: List["DrugOrder"]