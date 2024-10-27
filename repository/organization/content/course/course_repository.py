import bson
from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo.async_connection.connection.mongo_connection import get_database
from model.organization.content.course_model import Course
from typing import Optional, List

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
        course = await self.collection.find_one({"_id": bson.ObjectId(course_id)})
        if course:
            return Course(**course)
        return None

    async def get_courses_by_organization_id(self, organization_id: str) -> List[Course]:
        cursor = self.collection.find({"organization_id": organization_id})
        courses = await cursor.to_list(length=None)
        return [Course(**course) for course in courses]

    async def delete_course(self, course_id: str) -> bool:
        return await self.collection.delete_one({"_id": ObjectId(course_id)})


async def get_course_repository(db = Depends(get_database)) -> CourseRepository:
    return CourseRepository(db)