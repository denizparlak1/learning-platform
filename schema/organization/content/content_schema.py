from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class CourseCreate(BaseModel):
    title: str
    description: str
    organization_id: str
    access_level: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(arbitrary_types_allowed=True)

class SectionCreate(BaseModel):
    title: str
    description: str
    organization_id: str
    course_id: str
