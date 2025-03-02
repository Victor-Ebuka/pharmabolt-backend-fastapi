from pydantic import BaseModel, EmailStr
from typing import Optional

class MailingListBase(BaseModel):
    email: EmailStr

class MailingListCreate(MailingListBase):
    pass

class MailingListUpdate(BaseModel):
    email: Optional[EmailStr] = None

class MailingList(MailingListBase):
    id: int

    class Config:
        orm_mode = True
