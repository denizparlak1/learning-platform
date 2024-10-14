import string
import random
from core.security.security import SecurityUtils
from repository.organization.organization_repository import OrganizationUserRepository
from schema.organization.auth.organization_auth_schema import OrganizationUserCreate


class OrganizationUserService:
    def __init__(self, user_repo: OrganizationUserRepository):
        self.user_repo = user_repo

    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    async def create_user(self, user_info: OrganizationUserCreate):
        """Create a user for the organization."""
        user_info.password = self.generate_password()  # Auto-generate password
        print(user_info.password)
        # Hash the password before storing
        hashed_password = SecurityUtils.hash_password(user_info.password)
        user_info.password = hashed_password

        user_id = await self.user_repo.create_user(user_info)  # Store user with organization_id
        return {
            "user_id": user_id,
        }
