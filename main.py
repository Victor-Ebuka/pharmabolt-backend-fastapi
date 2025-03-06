from fastapi import FastAPI, Response
from database.session import Base, engine
from models import user, prescription, cart, order, drug, category, user, mailing_list, prescription_drug, drug_cart, drug_category, drug_order
from routes.users import router as users_router
from routes.drugs import router as drugs_router
from routes.auth import router as auth_router
from routes.carts import router as carts_router

app = FastAPI(
    title="PharmaBolt API",
    description="API for a PharmaBolt",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

@app.get("/")

def root():
    return Response("Server is running")


# app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(drugs_router)
app.include_router(carts_router)
