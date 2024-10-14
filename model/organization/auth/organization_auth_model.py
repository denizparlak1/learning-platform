from pydantic import BaseModel, EmailStr, Field

from core.validation.custom_validation import PyObjectId


class OrganizationAdminCreateInfo(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    organization_id: str
    name: str
    email: EmailStr
    password: str  # Password will be generated automatically in the service

