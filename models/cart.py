from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    total_price = Column(Integer, nullable=False)

    user = relationship("User", back_populates="cart")
    drugs = relationship("DrugCart", back_populates="cart")