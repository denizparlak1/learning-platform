from datetime import datetime
from typing import Optional

import bson
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate, \
    OrganizationUserCreate


class OrganizationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["organization-info"]

    async def create_organization(self, organization_data: OrganizationInfo):
        result = await self.collection.insert_one(organization_data.dict())
        return str(result.inserted_id)

    async def update_organization(self, organization_id: str, updates: dict):
        # Update only the fields that are not None
        update_data = {k: v for k, v in updates.items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update.")

        update_data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one(
            {"_id": organization_id}, {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Organization not found or no changes applied.")
        return True


class OrganizationAuthRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["organization-auth"]

    async def create_admin(self, admin_data: OrganizationAdminCreate):
        await self.collection.insert_one(admin_data.dict())

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def get_organization_id_by_user_id(self, user_id: str) -> Optional[str]:
        user = await self.collection.find_one({"_id": bson.ObjectId(user_id)}, {"organization_id": 1})
        return user["organization_id"] if user else None

    async def get_user_by_id(self, user_id: str):
        return await self.collection.find_one({"_id": bson.ObjectId(user_id)})

    async def update_password(self, user_id: str, hashed_password: str):
        await self.collection.update_one({"_id": user_id}, {"$set": {"password": hashed_password}})


class OrganizationUserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["organization-users-auth"]

    async def create_user(self, user_info: OrganizationUserCreate):
        user_data = user_info.dict()
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)