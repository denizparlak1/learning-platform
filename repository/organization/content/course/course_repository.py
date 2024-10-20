from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from model.organization.content.course_model import Course
from typing import Optional

from schema.organization.content.content_schema import CourseCreate


class CourseRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("organization-courses")

    async def create_course(self, course_data: CourseCreate) -> Course:
        course_dict = course_data.dict(by_alias=True)
        result = await self.collection.insert_one(course_dict)
        course_dict["_id"] = result.inserted_id
        return Course(**course_dict)

    async def get_course_by_id(self, course_id: ObjectId) -> Optional[Course]:
        course = await self.collection.find_one({"_id": course_id})
        if course:
            return Course(**course)
        return None

    async def update_course(self, course_id: ObjectId, course_data: dict) -> Optional[Course]:
        result = await self.collection.update_one({"_id": course_id}, {"$set": course_data})

        if result.matched_count == 0:
            return None

        updated_course = await self.get_course_by_id(course_id)
        return updated_course
