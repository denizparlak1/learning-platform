from repository.organization.organization_repository import OrganizationRepository
from schema.organization.info.organization_info_schema import OrganizationUpdate


class OrganizationInfoService:
    def __init__(self, org_repo: OrganizationRepository):
        self.org_repo = org_repo

    async def update_organization(self, organization_id: str, update_data: OrganizationUpdate):
        updates = update_data.dict(exclude_unset=True)
        return await self.org_repo.update_organization(organization_id, updates)
