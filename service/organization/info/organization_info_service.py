from datetime import datetime

from fastapi import HTTPException

from repository.organization.organization_repository import OrganizationRepository
from schema.organization.info.organization_info_schema import OrganizationUpdate


class OrganizationInfoService:
    def __init__(self, org_repo: OrganizationRepository):
        self.org_repo = org_repo

    async def update_organization(self, organization_id: str, update_data: OrganizationUpdate):
        updates = update_data.dict(exclude_unset=True)
        return await self.org_repo.update_organization(organization_id, updates)

    async def get_organization_info(self, organization_id: str):
        organization_info = await self.org_repo.get_organization_by_id(organization_id)
        if not organization_info:
            raise HTTPException(status_code=404, detail="Organization not found.")
        return organization_info
