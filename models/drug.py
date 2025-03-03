from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base

class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)

    categories = relationship("DrugCategory", back_populates="drug")
    prescriptions = relationship("PrescriptionDrug", back_populates="drug")
    orders = relationship("DrugOrder", back_populates="drug")
    carts = relationship("DrugCart", back_populates="drug")