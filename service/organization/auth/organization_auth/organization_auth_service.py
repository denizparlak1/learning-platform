import random
import string
from datetime import timedelta
from fastapi import HTTPException
from core.security.security import SecurityUtils
from repository.organization.organization_repository import OrganizationRepository, OrganizationAuthRepository
from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate

class OrganizationAuthService:
    def __init__(self, org_repo: OrganizationRepository, admin_repo: OrganizationAuthRepository):
        self.org_repo = org_repo
        self.admin_repo = admin_repo

    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    async def create_organization_and_admin(self, org_info: OrganizationInfo, admin_info: OrganizationAdminCreate):
        """Create an organization and its admin."""
        # Insert organization data
        org_id = await self.org_repo.create_organization(org_info)

        # Generate a password for the organization admin
        admin_info.password = self.generate_password()
        admin_info.password = SecurityUtils.hash_password(admin_info.password)

        # Ensure to set the organization name and role
        admin_info.organization_name = org_info.organization_name  # Assuming org_info has a 'name' field
        admin_info.role = "organization_admin"  # Ensure role is set

        await self.admin_repo.create_admin(admin_info)

        return {
            "organization_id": org_id,
        }

    async def login_organization_user(self, email: str, password: str):
        user = await self.admin_repo.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid email or password")

        if not SecurityUtils.verify_password(password, user["password"]):
            raise HTTPException(status_code=400, detail="Invalid email or password")

        token_data = {
            "sub": user["email"],
            "role": user["role"],
        }

        access_token_expires = timedelta(minutes=60)
        access_token = SecurityUtils.create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
