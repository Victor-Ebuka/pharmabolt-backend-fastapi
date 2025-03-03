from fastapi import APIRouter, Depends, status
from crud.cart import get_carts_by_drug_id
from crud.category import get_categories_by_drug_id
from database.session import get_db
from sqlalchemy.orm import Session

from crud.drugs import get_drugs, get_drug_by_id, add_drug, update_drug, delete_drug
from models.drug import Drug
from schemas.drug import DrugCreate, DrugDetailedResponse, DrugUpdate, DrugResponse

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"]
)

# Add a new drug
@router.post("/", response_model=DrugResponse, status_code=status.HTTP_201_CREATED)
def create_drug(drug: DrugCreate, db: Session = Depends(get_db)) -> Drug:
    new_drug = add_drug(db, drug)
    return new_drug

# Get all drugs
@router.get("/", response_model=list[DrugResponse])
def read_drugs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    drugs = get_drugs(skip, limit, db)
    return drugs

# Get a specific drug by ID
@router.get("/{drug_id}", response_model=DrugDetailedResponse)
def read_drug(drug_id: int, db: Session = Depends(get_db)):
    drug = get_drug_by_id(drug_id, db)
    categories = get_categories_by_drug_id(drug_id, db)
    carts = get_carts_by_drug_id(drug_id, db)

    drug.categories = categories
    drug.carts = carts
    return drug

# Update a specific drug by ID
@router.put("/{drug_id}", response_model=DrugResponse)
def update_drug_route(drug_id: int, drug: DrugUpdate, db: Session = Depends(get_db)):
    updated_drug = update_drug(drug_id, db, drug)
    return updated_drug

# Delete a specific drug by ID
@router.delete("/{drug_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_drug_in_db(drug_id: int, db: Session = Depends(get_db)):
    delete_drug(drug_id, db)
    return