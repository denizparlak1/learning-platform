from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from core.security.dependencies import permission_required, get_current_active_user
from db.mongo.connection.mongo_connection import get_database
from mail.service.postmark_service import PostmarkService
from repository.organization.organization_repository import OrganizationRepository, OrganizationAuthRepository, \
    OrganizationUserRepository
from schema.organization.auth.organization_auth_schema import OrganizationInfo, OrganizationAdminCreate, \
    OrganizationLoginSchema, OrganizationUserCreate, UpdateOrganizationAdminPasswordRequest, \
    OrganizationResetPasswordRequest
from service.organization.auth.organization_auth.organization_auth_service import OrganizationAuthService
from service.organization.auth.user_auth.organization_user_auth_service import OrganizationUserService

router = APIRouter()

@router.post("/sign-up/")
@permission_required("create_organization")
async def create_organization_api(
    organization_info: OrganizationInfo,
    admin_info: OrganizationAdminCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    org_repo = OrganizationRepository(db)
    admin_repo = OrganizationAuthRepository(db)
    service = OrganizationAuthService(org_repo, admin_repo)
    result = await service.create_organization_and_admin(organization_info, admin_info)
    return {"organization_id": result["organization_id"]}

@router.post("/sign-in")
async def login_organization_user(
    login_data: OrganizationLoginSchema,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    org_repo = OrganizationRepository(db)
    admin_repo = OrganizationAuthRepository(db)
    service = OrganizationAuthService(org_repo, admin_repo)
    result = await service.login_organization_user(login_data.email, login_data.password)
    return result


@router.post("/create-user/")
@permission_required("create_user")
async def create_user(
        user_info: OrganizationUserCreate,
        current_user: dict = Depends(get_current_active_user),
        db: AsyncIOMotorDatabase = Depends(get_database)
):
    user_repo = OrganizationUserRepository(db)
    auth_repo = OrganizationAuthRepository(db)
    mail_service = PostmarkService()
    service = OrganizationUserService(user_repo, mail_service)

    organization_id = await auth_repo.get_organization_id_by_user_id(current_user["_id"])

    user_info.organization_id = organization_id

    result = await service.create_user(user_info)
    return {"user_id": result["user_id"]}

@router.post("/reset-password")
async def reset_organization_admin_password(
    request: OrganizationResetPasswordRequest,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """
    Endpoint for resetting the password of an organization admin user.
    Requires the special access key in the header for security.
    """
    org_repo = OrganizationRepository(db)
    admin_repo = OrganizationAuthRepository(db)
    service = OrganizationAuthService(org_repo, admin_repo)
    return await service.reset_password(email=request.email)

@router.put("/update-password")
async def update_organization_admin_password(
    request:UpdateOrganizationAdminPasswordRequest,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """
    Endpoint for updating the password of an organization admin user.
    Requires the special access key in the header for security.
    """
    org_admin_service = OrganizationAuthService(db)
    return await org_admin_service.update_password(user_id=current_user["_id"], current_password=request.current_password, new_password=request.new_password)
