import random
import string
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr
from fastapi import HTTPException, Header
from datetime import datetime, timedelta

from config.enviroment.env_config import settings
from core.security.security import SecurityUtils
from mail.service.postmark_service import PostmarkService


class AdminAuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db["admin-auth"]
        self.access_key = "header-secret"  # Predefined access key
        self.mail_service = PostmarkService()

    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))


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
            data={"sub": admin["email"], "role": admin["role"], "_id": str(admin["_id"])},
            expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    async def reset_password(self, email: EmailStr, access_key: str = Header(...)):
        # Validate the special access key in the header
        if access_key != self.access_key:
            raise HTTPException(status_code=403, detail="Invalid access key.")

        # Find the admin by email
        admin = await self.collection.find_one({"email": email})
        if not admin:
            return True  # To prevent user enumeration attacks, return True even if the admin doesn't exist.

        # Generate a new password
        new_password = self.generate_password()

        # Hash the new password
        hashed_password = SecurityUtils.hash_password(new_password)

        # Update the admin's password in the database
        await self.collection.update_one(
            {"_id": admin["_id"]},
            {"$set": {"password": hashed_password, "updated_at": datetime.utcnow()}}
        )

        # Prepare the email content using a template (Postmark)
        template_model = {
            "name": admin["name"],
            "email": admin["email"],
            "new_password": new_password
        }

        # Send the new password via email using Postmark
        await self.mail_service.send_with_template(
            template_id=settings.POSTMARK_RESET_PASSWORD_TEMPLATE,
            to_address=admin["email"],
            template_model=template_model
        )
        return True

    async def update_password(self, email: str, current_password: str, new_password: str):
        # Find the admin by email
        admin = await self.collection.find_one({"email": email})
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found.")

        # Verify current password
        if not SecurityUtils.verify_password(current_password, admin["password"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect.")

        # Hash the new password
        hashed_new_password = SecurityUtils.hash_password(new_password)

        # Update the password in the database
        await self.collection.update_one(
            {"email": email},
            {"$set": {"password": hashed_new_password, "updated_at": datetime.utcnow()}}
        )

        # Send new password via email
        await self.mail_service.send_with_template(
            to_address=admin["email"],
            template_id=settings.POSTMARK_RESET_PASSWORD_TEMPLATE,
            template_model={
                "name": admin["name"],
                "new_password": new_password
            }
        )

        return True
