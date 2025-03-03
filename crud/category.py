from database.session import get_db
from models.category import Category
from models.drug_category import DrugCategory
from models.drug import Drug
from sqlalchemy.orm import Session
from fastapi import HTTPException
from schemas.category import CategoryCreate, CategoryUpdate


def get_categories(db: Session) -> list[Category]:
    categories = db.query(Category).all()
    return categories

def get_category_by_id(category_id: int, db: Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def get_categories_by_drug_id(drug_id: int, db: Session) -> list[Category]:
    categories = db.query(Category).join(DrugCategory, DrugCategory.category_id == Category.id).filter(DrugCategory.drug_id == drug_id).all()
    return categories