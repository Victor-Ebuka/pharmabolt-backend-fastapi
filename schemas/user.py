from typing import Annotated, Literal, Optional, List
from pydantic import BaseModel, EmailStr, Field
from schemas.cart import Cart
from schemas.order import UserOrder
from schemas.prescription import UserPrescription

# Base Schema
class UserBase(BaseModel):
    full_name: Annotated[str, Field(max_length=255)]
    email: EmailStr
    phone_no: Annotated[str, Field(max_length=255)]
    address: Annotated[str, Field(max_length=255)]
    city: Annotated[str, Field(max_length=255)]
    state: Annotated[str, Field(max_length=255)]
    role: Literal["user", "admin"] = "user"

# Schema for Creating User
class UserCreate(UserBase):
    password: Annotated[str, Field(max_length=255)]

# Schema for Updating User
class UserUpdate(BaseModel):
    full_name: Optional[str]
    phone_no: Optional[str]
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    role: Optional[str]

# Schema for Returning User Data
class UserResponse(UserBase):
    id: int
    prescriptions: List["UserPrescription"]
    orders: List["UserOrder"]
    cart: "Cart"

    class Config:
        from_attributes = True
