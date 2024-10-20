from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Annotated
from bson import ObjectId
from datetime import datetime

from core.validation.custom_validation import ObjectIdPydanticAnnotation


class Section(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    title: str
    description: str
    organization_id:str
    course_id:str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Course(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    title: str
    description: str
    organization_id: str
    access_level: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Video(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    video_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='video_id')
    title: str
    description: Optional[str] = None
    file_url: str
    section_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class Resource(BaseModel):
    id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='_id')
    resource_id: Annotated[ObjectId, ObjectIdPydanticAnnotation] = Field(alias='resource_id')
    title: str
    file_url: str
    section_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)
