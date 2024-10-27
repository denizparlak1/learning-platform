import asyncio
from typing import List
from bson import ObjectId
from model.organization.content.course_model import Course
from fastapi import HTTPException, Depends
from repository.organization.content.course.course_repository import CourseRepository, get_course_repository
from service.organization.content.section.organization_section_service import SectionService, get_section_service
from service.s3.s3_service import S3Service, get_s3_service


class CourseService:
    def __init__(self, course_repository: CourseRepository,section_service: SectionService,s3_service: S3Service):
        self.course_repository = course_repository
        self.section_service = section_service
        self.s3_service = s3_service

    async def create_course(self, course_data: Course) -> Course:
        return await self.course_repository.create_course(course_data)

    async def get_course_by_id(self, course_id: ObjectId) -> Course:
        course = await self.course_repository.get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    async def get_courses_by_organization_id(self, organization_id: str) -> List[Course]:
        courses = await self.course_repository.get_courses_by_organization_id(organization_id)
        if not courses:
            raise HTTPException(status_code=404, detail="No courses found for this organization")
        return courses

    async def delete_course_with_content(self, course_id: str) -> bool:
        info = await self.course_repository.get_course_by_id(course_id)
        s3_prefix = f"{info.organization_id}/content/{course_id}/"
        self.s3_service.delete_course_by_prefix(s3_prefix)

        sections = await self.section_service.get_sections(course_id)

        delete_tasks = [
            self.section_service.delete_section_with_content(section.id)
            for section in sections
        ]

        await asyncio.gather(*delete_tasks)

        return await self.course_repository.delete_course(course_id)



def get_course_service(
    course_repository: CourseRepository = Depends(get_course_repository),
    section_service: SectionService = Depends(get_section_service),s3_service: S3Service = Depends(get_s3_service)
) -> CourseService:
    return CourseService(course_repository, section_service,s3_service)