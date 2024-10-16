from model.organization.info.organization_info_model import Organization
from repository.admin.organization.info.admin_organization_info import AdminOrganizationRepository


class AdminOrganizationService:
    def __init__(self, organization_repo: AdminOrganizationRepository):
        self.organization_repo = organization_repo

    async def get_all_organizations(self):
        """Fetch all organizations and map to response model."""
        organizations = await self.organization_repo.list_organizations()
        return [Organization(**org) for org in organizations]

    async def update_organization_and_admin_status(self, organization_id: str, is_active: bool):
        """Update both organization and organization admin status."""
        # Update organization status
        organization_updated = await self.organization_repo.update_organization_status(organization_id, is_active)

        # Update organization admin status
        admin_updated = await self.organization_repo.update_organization_admin_status(organization_id, is_active)

        return {
            "organization_updated": organization_updated,
            "admin_updated": admin_updated,
            "message": "Organization and admin status updated successfully."
        }

    async def get_organizations_users_count(self):
        """
        Get the total number of users for each organization.
        This function aggregates the user count for all organizations.
        """
        return await self.organization_repo.get_organizations_users_count()

