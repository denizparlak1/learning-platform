from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class OrganizationInfo(BaseModel):
    organization_name: str
    description: str
    country: str
    city: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    subscription_date: datetime = Field(default_factory=datetime.utcnow)
    organization_admin_name: str
    organization_email: EmailStr

class OrganizationAdminCreate(BaseModel):
    name: str
    organization_name: str
    email: EmailStr
    password: str = None
    role: str = "organization_admin"


class OrganizationLoginSchema(BaseModel):
    email: str
    password: str