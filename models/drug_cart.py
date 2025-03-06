from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base


class DrugCart(Base):
    __tablename__ = "drugs_carts"

    id = Column(Integer, primary_key=True, index=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), nullable=False)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    drug = relationship("Drug", back_populates="carts")
    cart = relationship("Cart", back_populates="drugs")
