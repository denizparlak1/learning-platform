import random
import string

import bson
from fastapi import HTTPException, status
from datetime import timedelta

from config.enviroment.env_config import settings
from core.security.security import SecurityUtils

class UserAuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo


    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    async def login(self, email: str, password: str):
        """
        Log in a user with the provided email and password.
        """
        # Retrieve the user by email
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        # Verify the provided password
        if not SecurityUtils.verify_password(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        # Prepare the JWT token payload
        token_data = {
            "_id":str(user["_id"]),
            "sub": user["email"],
            "role": user["role"],
            "organization_id": user["organization_id"],  # Include organization_id in token
        }
        # Create the access token with expiration time
        access_token_expires = timedelta(minutes=30)
        access_token = SecurityUtils.create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

    async def reset_password(self, email: str, email_service):
        """
        Reset a user's password and send the new password via email.
        """
        user = await self.get_user_by_email(email)
        if not user:
            return True
            # To protect end user and mail services, return True to avoid exposing existence of user.

        new_password = self.generate_password()  # Generate new random password
        hashed_password = SecurityUtils.hash_password(new_password)  # Hash the new password

        # Update the user's password in the database
        await self.user_repo.update_user_password(user["_id"], hashed_password)
        print(new_password)

        # Send the new password via email using Postmark template
        await email_service.send_with_template(
            to_address=user["email"],
            template_id=settings.POSTMARK_RESET_PASSWORD_TEMPLATE,
            template_model={
                "name": user["name"],
                "new_password": new_password
            }  # Template model with the new password and user's name
        )

        return True


    async def update_password(self, user_id: str, current_password: str, new_password: str):
        """
        Update the user's password after verifying the current password.
        """

        user = await self.user_repo.get_user_by_id(bson.ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify the current password
        if not SecurityUtils.verify_password(current_password, user["password"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        # Hash the new password
        hashed_new_password = SecurityUtils.hash_password(new_password)

        # Update the user's password in the database
        await self.user_repo.update_user_password(user["_id"], hashed_new_password)

        return True


    async def get_user_by_email(self, email: str):
        """
        Helper method to retrieve user by email.
        """
        return await self.user_repo.get_user_by_email(email)

    async def get_user_by_id(self, user_id: str):
        """
        Retrieve user information by their unique ID.
        """
        return await self.user_repo.get_user_by_id(user_id)
