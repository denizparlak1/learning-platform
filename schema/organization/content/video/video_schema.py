from fastapi import UploadFile
from pydantic import BaseModel


class UploadVideoRequest(BaseModel):
    organization_id: str
    course_id: str
    section_id: str
    file: UploadFile