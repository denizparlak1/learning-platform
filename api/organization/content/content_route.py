from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase

from service.organization.content.video.video_service import VideoService, get_video_service
from tasks.video.video_tasks import upload_video_to_s3_task
from core.security.dependencies import permission_required, get_current_active_user
from db.mongo.async_connection.connection.mongo_connection import get_database
from repository.organization.content.course.course_repository import CourseRepository
from repository.organization.content.section.section_repository import SectionRepository
from schema.organization.content.content_schema import CourseCreate, SectionCreate
from service.organization.content.course.organization_course_service import CourseService, get_course_service
from service.organization.content.section.organization_section_service import SectionService, get_section_service

router = APIRouter()

@router.post("/create-course")
@permission_required("content_creator")
async def create_course(course: CourseCreate, db: AsyncIOMotorDatabase = Depends(get_database),service: CourseService = Depends(get_course_service),
                        current_user: dict = Depends(get_current_active_user)):
    return await service.create_course(course)


@router.post("/create-section")
@permission_required("content_creator")
async def create_section(section: SectionCreate,db: AsyncIOMotorDatabase = Depends(get_database),service: SectionService = Depends(get_section_service),
                         current_user: dict = Depends(get_current_active_user)):
    return await service.create_section(section)


@router.post("/upload-video")
@permission_required("ORG_ADMIN")
async def upload_video(
    organization_id: str = Form(...),
    course_id: str = Form(...),
    file: UploadFile = Form(...),
    section_id: str = Form(...),
    is_public:  bool = Form(...),
    current_user: dict = Depends(get_current_active_user)
):
    try:
        file_content = await file.read()
        content_type = file.content_type

        result = upload_video_to_s3_task.delay(
            organization_id, course_id, file_content, file.filename, content_type,is_public,section_id
        )

        return {"message": f"Video upload started. Task ID: {result.id}. You can check Celery logs for progress."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/courses/{organization_id}")
@permission_required("ORG_ADMIN")
async def get_courses_api(organization_id: str, course_service: CourseService = Depends(get_course_service),
                          current_user: dict = Depends(get_current_active_user)):
    return await course_service.get_courses_by_organization_id(organization_id)

@router.get("/section/{course_id}")
@permission_required("ORG_ADMIN")
async def get_courses_api(course_id: str, section_service: SectionService = Depends(get_section_service),
                          current_user: dict = Depends(get_current_active_user)):
    return await section_service.get_sections(course_id)

@router.get("/{section_id}")
@permission_required("ORG_ADMIN")
async def get_videos(section_id: str, video_service: VideoService = Depends(get_video_service),
                     current_user: dict = Depends(get_current_active_user)):
    return await video_service.get_videos_by_section_id(section_id)

@router.delete("/video/{video_id}", response_description="Delete a video")
@permission_required("ORG_ADMIN")
async def delete_video(video_id: str, video_service: VideoService = Depends(get_video_service),
                       current_user: dict = Depends(get_current_active_user)):
    deleted = await video_service.delete_video(video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"detail": "Video deleted successfully"}

@router.delete("/section/{section_id}", response_description="Delete a section and its content")
@permission_required("ORG_ADMIN")
async def delete_section(section_id: str, section_service: SectionService = Depends(get_section_service),
                         current_user: dict = Depends(get_current_active_user)):
    deleted = await section_service.delete_section_with_content(section_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Section not found or could not be deleted")
    return {"detail": "Section and its content deleted successfully"}

@router.delete("/course/{course_id}")
@permission_required("ORG_ADMIN")
async def delete_course(course_id: str, course_service: CourseService = Depends(get_course_service),
                        current_user: dict = Depends(get_current_active_user)):
    deleted = await course_service.delete_course_with_content(course_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Course not found or could not be deleted")
    return {"detail": "Course and its content deleted successfully"}
