from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.session import Base

class PrescriptionDrug(Base):
    __tablename__ = "prescription_drug"

    id = Column(Integer, primary_key=True, index=True)
    prescription_id = Column(Integer, ForeignKey("prescriptions.id"))
    drug_id = Column(Integer, ForeignKey("drugs.id"))
    dosage = Column(String, nullable=False)  # e.g., "500mg", "2 tablets"
    instructions = Column(Text)  # e.g., "Take after meals"

    prescription = relationship("Prescription", back_populates="drugs")
    drug = relationship("Drug", back_populates="prescriptions")