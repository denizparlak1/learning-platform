from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Admin Auth Model
class AdminModel(BaseModel):
    name: str
    email: EmailStr
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    role: str = "software_admin"

    class Config:
        orm_mode = True
