from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class Category(CategoryBase):
    id: int
    drugs: List["DrugCategory"]  # Added relationship with drugs

    class Config:
        orm_mode = True

class DrugCategoryBase(BaseModel):
    drug_id: int
    category_id: int

class DrugCategory(DrugCategoryBase):
    id: int

    class Config:
        orm_mode = True
