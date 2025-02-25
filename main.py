from fastapi import FastAPI
from app.db.base import Base, engine
from app.db.models import User, Cart, Prescription, Order, Category, Drug, MailingList, DrugCart, DrugCategory, DrugOrder, DrugPrescription
from app.routes import prescriptions, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

# app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
# app.include_router(users.router, prefix="/users", tags=["Users"])
