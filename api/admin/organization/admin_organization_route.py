from typing import List
from fastapi import APIRouter, Depends, Body
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.security.dependencies import permission_required, get_current_active_user
from db.mongo.async_connection.connection.mongo_connection import get_database
from model.organization.info.organization_info_model import Organization
from repository.admin.organization.info.admin_organization_info import AdminOrganizationRepository
from schema.admin.info.admin_organizations_info import AdminOrganizationUserCount
from service.admin.organization.info.admin_organization_service import AdminOrganizationService

router = APIRouter()

@router.get("/list-organizations", response_model=List[Organization])
@permission_required("list_organizations")
async def list_organizations(
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    organization_repo = AdminOrganizationRepository(db)
    service = AdminOrganizationService(organization_repo)

    organizations = await service.get_all_organizations()

    return organizations


@router.put("/update/{organization_id}", summary="Update organization and admin status")
@permission_required("ADMIN_ACCESS")
async def update_organization_status_api(
        organization_id: str,
        is_active: bool = Body(..., embed=True, description="Active status to update"),
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    organization_repo = AdminOrganizationRepository(db)
    organization_service = AdminOrganizationService(organization_repo)

    # Update organization and admin status
    result = await organization_service.update_organization_and_admin_status(organization_id, is_active)
    return result


@router.get("/users-count", response_model=List[AdminOrganizationUserCount])
async def get_organizations_users_count(db: AsyncIOMotorDatabase = Depends(get_database)):
    """
    API endpoint to get the total user count for each organization.
    """
    organization_repo = AdminOrganizationRepository(db)
    service = AdminOrganizationService(organization_repo)
    return await service.get_organizations_users_count()
