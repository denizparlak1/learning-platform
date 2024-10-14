from typing import Optional

from pydantic import BaseModel, Field


class OrganizationUpdate(BaseModel):
    description: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    organization_admin_name: Optional[str] = Field(None, alias="organization_admin_name")
