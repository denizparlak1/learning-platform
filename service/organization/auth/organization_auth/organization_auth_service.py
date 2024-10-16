import random
import string
from datetime import timedelta, datetime
from fastapi import HTTPException

from config.enviroment.env_config import settings
from core.security.security import SecurityUtils
from mail.service.postmark_service import PostmarkService
from repository.organization.organization_repository import OrganizationRepository, OrganizationAuthRepository
from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate

class OrganizationAuthService:
    def __init__(self, org_repo: OrganizationRepository, admin_repo: OrganizationAuthRepository):
        self.org_repo = org_repo
        self.admin_repo = admin_repo
        self.mail_service = PostmarkService()

    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    async def create_organization_and_admin(self, org_info: OrganizationInfo, admin_info: OrganizationAdminCreate):
        """Create an organization and its admin."""
        # Generate unique organization_id and assign it to both organization and admin
        org_id = org_info.organization_id  # UUID is generated in OrganizationInfo by default

        # Insert organization data with the unique organization_id
        await self.org_repo.create_organization(org_info)

        # Generate a password for the organization admin
        admin_info.password = self.generate_password()
        print(admin_info.password)
        admin_info.password = SecurityUtils.hash_password(admin_info.password)

        # Assign the same organization_id to the admin user
        admin_info.organization_id = org_id
        admin_info.organization_name = org_info.organization_name
        admin_info.role = "organization_admin"

        # Create admin in the database
        await self.admin_repo.create_admin(admin_info)

        return {
            "organization_id": org_id,  # Return unique organization_id
        }

    async def login_organization_user(self, email: str, password: str):
        user = await self.admin_repo.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        if not SecurityUtils.verify_password(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token_data = {
            "_id":str(user["_id"]),
            "sub": user["email"],
            "role": user["role"],
        }

        access_token_expires = timedelta(minutes=60)
        access_token = SecurityUtils.create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

    async def reset_password(self, email: str):
        """Reset password for an organization admin user."""
        user = await self.admin_repo.get_user_by_email(email)
        if not user:
            return True  # To avoid exposing the existence of the user

        # Generate a new password
        new_password = self.generate_password()
        print(new_password)
        hashed_password = SecurityUtils.hash_password(new_password)

        # Update the password in the database
        await self.admin_repo.update_password(user["_id"], hashed_password)

        # Send the new password to the user via email
        await self.mail_service.send_with_template(
            to_address=user["email"],
            template_id=settings.POSTMARK_RESET_PASSWORD_TEMPLATE,
            template_model={
                "name": user["name"],
                "email": user["email"],
                "new_password": new_password
            }
        )

        return True

    async def update_password(self, user_id: str, current_password: str, new_password: str):
        """Update the password of an organization admin user."""
        user = await self.admin_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify the current password
        if not SecurityUtils.verify_password(current_password, user["password"]):
            raise HTTPException(status_code=400, detail="Current password is incorrect")

        # Hash the new password and update it
        hashed_new_password = SecurityUtils.hash_password(new_password)
        await self.admin_repo.update_password(user_id, hashed_new_password)

        # Send the new password via email
        await self.mail_service.send_with_template(
            to_address=user["email"],
            template_id=settings.POSTMARK_UPDATE_PASSWORD_TEMPLATE,
            template_model={
                "name": user["name"],
                "new_password": new_password
            }
        )

        return True
