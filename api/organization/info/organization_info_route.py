from typing import List

from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.security.dependencies import get_current_active_user, permission_required
from db.mongo.async_connection.connection.mongo_connection import get_database
from model.organization.info.organization_info_model import Organization
from repository.organization.common.organization_repository import OrganizationRepository, OrganizationAuthRepository, \
    OrganizationUserRepository
from schema.organization.info.organization_info_schema import OrganizationUpdate, OrganizationUserInfoResponse, \
    UpdateUserStatusRequest
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


@router.get("/{organization_id}", response_model=Organization)
@permission_required("view_organization")
async def get_organization_info(
        organization_id: str,
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    org_repo = OrganizationRepository(db)
    org_service = OrganizationInfoService(org_repo)

    organization_info = await org_service.get_organization_info(organization_id)
    return organization_info


@router.get("/users/", response_model=List[OrganizationUserInfoResponse])

async def get_organization_users(
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    auth_repo = OrganizationAuthRepository(db)
    organization_id = await auth_repo.get_organization_id_by_user_id(current_user["_id"])

    user_repo = OrganizationUserRepository(db)
    users = await user_repo.get_users_by_organization_id(organization_id)
    return users

@router.put("/update-user-status/{user_id}")
@permission_required("update_user_status")
async def update_user_status(
        user_id: str,
        update_data: UpdateUserStatusRequest,
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = OrganizationUserRepository(db)

    result = await user_repo.update_user_status(user_id, update_data.is_active)

    if result.modified_count == 1:
        return {"message": "User status updated successfully."}
    return {"message": "Failed to update user status or no changes made."}

