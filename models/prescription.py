from sqlalchemy import Column, Date, ForeignKey, Integer, String, Text, Sequence
from sqlalchemy.orm import relationship
from database.session import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    prescription_date = Column(Date, nullable=False)
    instructions = Column(Text)

    user = relationship("User", back_populates="prescriptions")
    drugs = relationship("PrescriptionDrug", back_populates="prescription")
    