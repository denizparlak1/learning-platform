from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase


class AdminOrganizationRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.org_collection = db.get_collection("organization-info")
        self.org_admin_user_collection = db.get_collection("organization-auth")
        self.org_user_collection = db.get_collection("organization-users-auth")

    async def list_organizations(self):
        """List all organizations from the database."""
        cursor = self.org_collection.find({})
        organizations = await cursor.to_list(None)
        return organizations

    async def update_organization_status(self, organization_id: str, is_active: bool):
        """Update the status of the organization (is_active field)."""
        result = await self.org_collection.update_one(
            {"organization_id": organization_id},
            {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Organization not found or no changes applied.")
        return True

    async def update_organization_admin_status(self, organization_id: str, is_active: bool):
        """Update the status of the organization admin (is_active field)."""
        result = await self.org_admin_user_collection.update_one(
            {"organization_id": organization_id},
            {"$set": {"is_active": is_active, "updated_at": datetime.utcnow()}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Organization admin not found or no changes applied.")
        return True


    async def get_organizations_users_count(self):
        """
        Retrieve the total number of users for each organization from the organization-auth collection.
        Uses aggregation to group by organization_id and count the number of users.
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$organization_id",
                    "total_users": {"$sum": 1}
                }
            }
        ]
        result = await self.org_user_collection.aggregate(pipeline).to_list(None)

        return [{"organization_id": str(item["_id"]), "total_users": item["total_users"]} for item in result]
