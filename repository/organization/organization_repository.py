import bson
from motor.motor_asyncio import AsyncIOMotorDatabase

from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate, \
    OrganizationUserCreate


class OrganizationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["organization-info"]

    async def create_organization(self, organization_data: OrganizationInfo):
        result = await self.collection.insert_one(organization_data.dict())
        return str(result.inserted_id)

class OrganizationAuthRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["organization-auth"]

    async def create_admin(self, admin_data: OrganizationAdminCreate):
        await self.collection.insert_one(admin_data.dict())

    async def get_user_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

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