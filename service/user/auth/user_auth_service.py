from fastapi import HTTPException, status
from datetime import timedelta
from core.security.security import SecurityUtils

class UserAuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

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
            "email": user["email"],
            "role": user["role"],
            "organization_id": user["organization_id"],  # Include organization_id in token
        }

        # Create the access token with expiration time
        access_token_expires = timedelta(minutes=30)
        access_token = SecurityUtils.create_access_token(
            data=token_data, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

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
