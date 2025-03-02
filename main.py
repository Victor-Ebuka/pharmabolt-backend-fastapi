from fastapi import FastAPI, Response
from database.session import Base, engine
from models import user, prescription, cart, order, drug, category, user, mailing_list, prescription_drug, drug_cart, drug_category, drug_order
from routes.users import router as users_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

# app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(users_router)


@app.get("/")
def root():
    return Response("Server is running")

import json
from sqlalchemy.orm import Session
from database.session import SessionLocal
from models.drug import Drug

def backup_drugs():
    db: Session = SessionLocal()
    drugs = db.query(Drug).all()
    drugs_data = [{"id": d.id, "name": d.name} for d in drugs]  # Convert to dictionary
    
    with open("backup_drugs.json", "w") as f:
        json.dump(drugs_data, f, indent=4)

    db.close()
    print("Backup completed.")


backup_drugs()