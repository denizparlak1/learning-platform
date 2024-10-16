from typing import Annotated
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field
from core.validation.custom_validation import ObjectIdPydanticAnnotation


class OrganizationAdminCreateInfo(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    organization_id: str
    name: str
    email: EmailStr
    password: str  # Password will be generated automatically in the service

