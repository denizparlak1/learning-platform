from motor.motor_asyncio import AsyncIOMotorDatabase

from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate


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
