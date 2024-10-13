from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from core.validation.custom_validation import PyObjectId


# Model for the stored organization in the database
class Organization(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    organization_name: str
    description: str
    country: str
    city: str
    created_at: datetime
    updated_at: datetime
    subscription_date: datetime
    organization_admin_name: str
    organization_email: EmailStr
