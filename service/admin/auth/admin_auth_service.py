from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from core.security.security import SecurityUtils  # Import the new SecurityUtils class

class AdminAuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["admin-auth"]
        self.access_key = "header-secret"  # Predefined access key

    async def signup(self, name: str, email: EmailStr, password: str, access_key: str = Header(...)):
        # Validate access key
        if access_key != self.access_key:
            raise HTTPException(status_code=403, detail="Invalid access key.")

        # Check if the admin already exists
        existing_admin = await self.collection.find_one({"email": email})
        if existing_admin:
            raise HTTPException(status_code=400, detail="Admin with this email already exists.")

        # Hash the password
        hashed_password = SecurityUtils.hash_password(password)

        # Create the admin data
        admin_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "role": "software_admin"
        }
        await self.collection.insert_one(admin_data)
        return {"message": "Admin created successfully."}

    async def signin(self, email: EmailStr, password: str):
        # Find the admin by email
        admin = await self.collection.find_one({"email": email})
        if not admin:
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        # Verify the password
        if not SecurityUtils.verify_password(password, admin["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password.")

        # Create a JWT token
        access_token_expires = timedelta(minutes=30)
        access_token = SecurityUtils.create_access_token(
            data={"sub": admin["email"], "role": admin["role"]},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
