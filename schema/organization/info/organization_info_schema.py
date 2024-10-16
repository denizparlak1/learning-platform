from datetime import datetime
from typing import Optional, Annotated

from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr

from core.validation.custom_validation import ObjectIdPydanticAnnotation


class OrganizationUpdate(BaseModel):
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    organization_admin_name: Optional[str] = Field(None, alias="organization_admin_name")

class OrganizationUserInfoResponse(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UpdateUserStatusRequest(BaseModel):
    is_active: bool