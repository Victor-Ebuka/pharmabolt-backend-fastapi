from typing import Annotated, Optional, List
from pydantic import BaseModel, Field

from schemas.cart import DrugCart
from schemas.category import DrugCategory
from schemas.order import DrugOrder

# Base Schema
class DrugBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    description: str
    price: Annotated[int, Field(ge=0)]  # Price should be non-negative
    stock: Annotated[int, Field(ge=0)]  # Stock should be non-negative

# Schema for Creating Drug
class DrugCreate(DrugBase):
    pass

# Schema for Updating Drug
class DrugUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=255)]]
    description: Optional[str]
    price: Optional[Annotated[int, Field(ge=0)]]
    stock: Optional[Annotated[int, Field(ge=0)]]

# Schema for Returning Drug Data
class DrugResponse(DrugBase):
    id: int
    categories: List["DrugCategory"]
    carts: List["DrugCart"]
    orders: List["DrugOrder"]

    class Config:
        from_attributes = True

