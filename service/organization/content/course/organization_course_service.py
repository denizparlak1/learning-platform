from bson import ObjectId
from model.organization.content.course_model import Course
from fastapi import HTTPException

from repository.organization.content.course.course_repository import CourseRepository


class CourseService:
    def __init__(self, course_repository: CourseRepository):
        self.course_repository = course_repository

    async def create_course(self, course_data: Course) -> Course:
        return await self.course_repository.create_course(course_data)

    async def get_course_by_id(self, course_id: ObjectId) -> Course:
        course = await self.course_repository.get_course_by_id(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course

    async def update_course(self, course_id: ObjectId, update_data: dict) -> Course:
        updated_course = await self.course_repository.update_course(course_id, update_data)
        if not updated_course:
            raise HTTPException(status_code=404, detail="Failed to update course")
        return updated_course
