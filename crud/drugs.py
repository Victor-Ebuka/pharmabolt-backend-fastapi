from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.drug import Drug
from models.drug_cart import DrugCart
from models.drug_category import DrugCategory
from models.drug_order import DrugOrder
from schemas.drug import DrugCreate, DrugUpdate
from models.prescription_drug import PrescriptionDrug

def add_drug(db: Session, drug: DrugCreate) -> Drug:
    db_drug = db.query(Drug).filter(Drug.name == drug.name).first()
    if db_drug:
        raise HTTPException(status_code=400, detail="Drug already exists")
    new_drug = Drug(**drug.model_dump())
    db.add(new_drug)
    db.commit()
    db.refresh(new_drug)
    return new_drug

def get_drugs(skip: int, limit: int, db: Session) -> list[Drug]:
    drugs = db.query(Drug).offset(skip).limit(limit).all()
    return drugs

def get_drug_by_id(drug_id: int, db: Session) -> Drug:
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    return drug

def update_drug(drug_id: int, db: Session, drug: DrugUpdate) -> Drug:
    db_drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    if db.query(Drug).filter(Drug.name == drug.name):
        raise HTTPException(status_code=400, detail=f"Drug {drug.name} exists")
    for key, value in drug.model_dump().items():
        setattr(db_drug, key, value)
    db.commit()
    db.refresh(db_drug)
    return db_drug

def delete_drug(drug_id: int, db: Session):
    db_drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not db_drug:
        raise HTTPException(status_code=404, detail="Drug not found")
    db.delete(db_drug)
    db.commit()
    return

def get_drugs_by_category_id(category_id: int, db: Session) -> list[Drug]:
    drugs = db.query(Drug).join(DrugCategory, DrugCategory.drug_id == Drug.id).filter(DrugCategory.category_id == category_id).all()
    return drugs

def get_drugs_by_order_id(order_id: int, db: Session) -> list[Drug]:
    drugs = db.query(Drug).join(DrugOrder, DrugOrder.drug_id == Drug.id).filter(DrugOrder.order_id == order_id).all()
    return drugs

def get_drugs_by_cart_id(cart_id: int, db: Session) -> list[Drug]:
    drugs = db.query(Drug).join(DrugCart, DrugCart.drug_id == Drug.id).filter(DrugCart.cart_id == cart_id).all()
    return drugs

def get_drugs_by_prescription_id(prescription_id: int, db: Session) -> list[Drug]:
    drugs = db.query(Drug).join(PrescriptionDrug, PrescriptionDrug.drug_id == Drug.id).filter(PrescriptionDrug.prescription_id == prescription_id).all()
    return drugs