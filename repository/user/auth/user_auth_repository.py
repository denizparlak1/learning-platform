from motor.motor_asyncio import AsyncIOMotorDatabase

class UserAuthRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        # Define the user collection
        self.collection = db.get_collection("organization-users-auth")

    async def update_user_password(self, user_id: str, new_password: str):
        """
        Update the user's password in the database.
        """
        await self.collection.update_one({"_id": user_id}, {"$set": {"password": new_password}})

    async def get_user_by_email(self, email: str):
        """
        Fetch a user by their email address.
        """
        return await self.collection.find_one({"email": email})

    async def get_user_by_id(self, user_id: str):
        """
        Fetch a user by their unique ID.
        """
        return await self.collection.find_one({"_id": user_id})

