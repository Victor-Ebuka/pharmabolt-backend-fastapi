from pydantic import BaseModel
from typing import Optional, List

class PrescriptionDrugBase(BaseModel):
    prescription_id: int
    drug_id: int
    dosage: str
    instructions: Optional[str]

class PrescriptionCreate(BaseModel):
    user_id: int
    drugs: List[PrescriptionDrugBase]

class PrescriptionUpdate(BaseModel):
    user_id: Optional[int] = None
    drugs: List[PrescriptionDrugBase]

class PrescriptionResponse(BaseModel):
    id: int
    user_id: int
    drugs: List[PrescriptionDrugBase]

    class Config:
        from_attributes = True

class UserPrescriptionBase(BaseModel):
    user_id: int
    prescription_id: int

class UserPrescription(UserPrescriptionBase):
    id: int

    class Config:
        orm_mode = True
