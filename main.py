from fastapi import FastAPI, Response
from database.session import Base, engine
from models import user, prescription, cart, order, drug, category, user, mailing_list, prescription_drug, drug_cart, drug_category, drug_order
from routes.users import router as users_router
from routes.drugs import router as drugs_router

app = FastAPI(
    title="PharmaBolt API",
    description="API for a PharmaBolt",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

# app.include_router(prescriptions.router, prefix="/prescriptions", tags=["Prescriptions"])
app.include_router(users_router)
app.include_router(drugs_router)


@app.get("/")
def root():
    return Response("Server is running")
