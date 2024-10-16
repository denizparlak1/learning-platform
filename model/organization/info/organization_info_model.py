from datetime import datetime
from typing import Annotated
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from core.validation.custom_validation import ObjectIdPydanticAnnotation


# Model for the stored organization in the database
class Organization(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    organization_id: str
    organization_name: str
    description: str
    country: str
    city: str
    created_at: datetime
    updated_at: datetime
    subscription_date: datetime
    organization_admin_name: str
    organization_email: EmailStr

class OrganizationUser(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    name: str
    email: EmailStr
    organization_id: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

