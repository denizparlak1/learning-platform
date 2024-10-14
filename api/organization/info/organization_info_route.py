from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.security.dependencies import get_current_active_user
from db.mongo.connection.mongo_connection import get_database
from repository.organization.organization_repository import OrganizationRepository
from schema.organization.info.organization_info_schema import OrganizationUpdate
from service.organization.info.organization_info_service import  OrganizationInfoService

router = APIRouter()

@router.put("/organization")
async def update_organization(
    update_data: OrganizationUpdate,
    db: AsyncIOMotorDatabase = Depends(get_database),
    current_user: dict = Depends(get_current_active_user),
):
    """
    API to update organization details (description, country, city, organization_admin_name).
    """
    org_repo = OrganizationRepository(db)
    org_service = OrganizationInfoService(org_repo)

    await org_service.update_organization(current_user["_id"], update_data)
    return True