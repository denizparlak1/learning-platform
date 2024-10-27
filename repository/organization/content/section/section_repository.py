import bson
from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.mongo.async_connection.connection.mongo_connection import get_database
from model.organization.content.course_model import Section
from schema.organization.content.content_schema import SectionCreate


class SectionRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("content-sections")

    async def create_section(self, section_data: SectionCreate) -> Section:
        section_dict = section_data.dict(by_alias=True)
        result = await self.collection.insert_one(section_dict)
        section_dict["_id"] = str(result.inserted_id)
        return Section(**section_dict)

    async def get_sections_by_course_id(self, course_id: str) -> Section:
        section = self.collection.find({"course_id": course_id})
        sections = await section.to_list(length=None)
        return [Section(**section) for section in sections]

    async def get_section_by_id(self, section_id: str) -> Section:
        section = await self.collection.find_one({"_id": bson.ObjectId(section_id)})
        if section:
            return Section(**section)
        return None

    async def update_section(self, section_id: str, section_data: SectionCreate):
        await self.collection.update_one({"_id": section_id}, {"$set": section_data.dict()})

    async def delete_section(self, section_id: str):
        return await self.collection.delete_one({"_id": bson.ObjectId(section_id)})

async def get_section_repository(db = Depends(get_database)) -> SectionRepository:
    return SectionRepository(db)