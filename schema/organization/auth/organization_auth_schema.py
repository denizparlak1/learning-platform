import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationInfo(BaseModel):
    organization_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_name: str
    description: str
    country: str
    city: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    subscription_date: datetime = Field(default_factory=datetime.utcnow)
    organization_admin_name: str
    organization_email: EmailStr
    is_active: bool = True

class OrganizationAdminCreate(BaseModel):
    name: str
    organization_name: str
    email: EmailStr
    password: str = None
    role: str = "organization_admin"
    organization_id: str = None
    is_active: bool = True
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class OrganizationLoginSchema(BaseModel):
    email: str
    password: str

class OrganizationUserCreate(BaseModel):
    email: EmailStr
    name: str
    organization_id: str
    organization_name: str
    password: Optional[str] = None
    is_active: bool = True
    role: str = "organization_user"
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class UpdateOrganizationAdminPasswordRequest(BaseModel):
    current_password: str
    new_password: str

class OrganizationResetPasswordRequest(BaseModel):
    email: EmailStr