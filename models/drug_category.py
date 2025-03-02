from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base

class DrugCategory(Base):
    __tablename__ = "drugs_categories"

    id = Column(Integer, primary_key=True, index=True)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    drug = relationship("Drug", back_populates="categories")
    category = relationship("Category", back_populates="drugs")