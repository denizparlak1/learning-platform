from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.security.dependencies import permission_required, get_current_active_user
from db.mongo.connection.mongo_connection import get_database
from repository.organization.content.course.course_repository import CourseRepository
from repository.organization.content.section.section_repository import SectionRepository
from schema.organization.content.content_schema import CourseCreate, SectionCreate
from service.organization.content.course.organization_course_service import CourseService
from service.organization.content.section.organization_section_service import SectionService
from service.organization.content.video.video_service import VideoService, get_video_service

router = APIRouter()

@router.post("/create-course")
@permission_required("content_creator")
async def create_course(course: CourseCreate, db: AsyncIOMotorDatabase = Depends(get_database), current_user: dict = Depends(get_current_active_user)):
    course_repo = CourseRepository(db)
    service = CourseService(course_repo)
    return await service.create_course(course)


@router.post("/create-section")
@permission_required("content_creator")
async def create_section(section: SectionCreate,db: AsyncIOMotorDatabase = Depends(get_database),current_user: dict = Depends(get_current_active_user)):
    section_repo = SectionRepository(db)
    service = SectionService(section_repo)
    return await service.create_section(section)

@router.post("/upload-video")
async def upload_video(
    organization_id: str = Form(...),
    course_id: str = Form(...),
    file: UploadFile = File(...),
    video_service: VideoService = Depends(get_video_service)
):
    try:
        video_id = await video_service.upload_video(
            organization_id,
            course_id,
            file
        )
        return {"video_id": video_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))