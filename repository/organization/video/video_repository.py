from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from bson import ObjectId

from db.mongo.async_connection.connection.mongo_connection import get_database
from model.organization.content.course_model import Video


class VideoRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.get_collection("organization-videos")

    def insert_video(self, video_data: dict) -> str:
        video_data['created_at'] = datetime.utcnow()
        video_data['updated_at'] = datetime.utcnow()
        result =  self.collection.insert_one(video_data)
        return str(result.inserted_id)

    async def get_video_by_id(self, video_id: str):
        return await self.collection.find_one({"_id": ObjectId(video_id)})

    async def get_videos_by_section_id(self, section_id: str) -> Video:
        resource = self.collection.find({"section_id": section_id})
        resource_result = await resource.to_list(length=None)
        return [Video(**resource) for resource in resource_result]

    async def delete_video(self, video_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(video_id)})
        return result.deleted_count > 0

    async def delete_videos_by_section_id(self, section_id: str) -> int:
        return await self.collection.delete_many({"section_id": section_id})


def get_video_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> VideoRepository:
    return VideoRepository(db)