import string
import random

from config.enviroment.env_config import settings
from core.security.security import SecurityUtils
from mail.service.postmark_service import PostmarkService
from repository.organization.common.organization_repository import OrganizationUserRepository
from schema.organization.auth.organization_auth_schema import OrganizationUserCreate


class OrganizationUserService:
    def __init__(self, user_repo: OrganizationUserRepository, mail_service: PostmarkService):
        self.user_repo = user_repo
        self.mail_service = mail_service

    def generate_password(self, length=8) -> str:
        """Generate a random password."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for i in range(length))

    async def create_user(self, user_info: OrganizationUserCreate):
        """Create a user for the organization."""
        plain_password = self.generate_password()  # Auto-generate password
        print(f"Generated password: {plain_password}")
        # Hash the password before storing
        hashed_password = SecurityUtils.hash_password(plain_password)
        user_info.password = hashed_password

        # Store user with organization_id
        user_id = await self.user_repo.create_user(user_info)

        # Prepare the email data using the welcome template
        template_model = {
            "name": user_info.name,
            "organization": user_info.organization_name,
            "email": user_info.email,
            "password": plain_password
        }

        # Send welcome email with credentials
        await self.mail_service.send_with_template(
            template_id=settings.POSTMARK_WELCOME_TEMPLATE_ID,
            to_address=user_info.email,
            template_model=template_model
        )

        return {
            "user_id": user_id,
        }
